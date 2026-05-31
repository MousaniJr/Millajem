"""
Scraper de feeds RSS de blogs de viajes y puntos.
Carga feeds desde la base de datos (tabla sources) con fallback a feeds hardcodeados.
"""
import feedparser
from bs4 import BeautifulSoup
from typing import List, Dict, Optional, Tuple
from datetime import datetime
import re


class RSSFeedScraper:
    """Scraper de feeds RSS de blogs de viajes"""

    # Feeds hardcodeados como fallback si la BD esta vacia
    FALLBACK_FEEDS = {
        "puntos_viajeros": "https://puntosviajeros.com/feed/",
        "travel_dealz": "https://travel-dealz.com/feed/",
        "head_for_points": "https://www.headforpoints.com/feed/",
        "insideflyer_uk": "https://www.insideflyer.co.uk/feed/",
        "turning_left_less": "https://www.turningleftforless.com/feed/",
        "one_mile_time": "https://onemileatatime.com/feed/",
        "the_points_guy": "https://thepointsguy.com/feed/",
        "frequent_miler": "https://frequentmiler.com/feed/",
        "melhores_destinos": "https://www.melhoresdestinos.com.br/feed",
        "passageiro_primeira": "https://passageirodeprimeira.com/feed/",
        "pontos_voar": "https://pontospravoar.com/feed/",
        "blog_maxmilhas": "https://blog.maxmilhas.com.br/feed/",
    }

    # Palabras clave para detectar promociones relevantes
    KEYWORDS = {
        "bonus": ["bonus", "bonus", "bonificacion", "bonificacao", "bônus"],
        "avios": ["avios", "iberia", "british airways", "ba", "vueling"],
        "transfer": ["transferencia", "transferencia", "transfer", "conversao", "conversion"],
        "purchase": ["compra", "buy", "comprar"],
        "promo": ["promocion", "promocao", "promo", "oferta", "deal"],
        "livelo": ["livelo"],
        "esfera": ["esfera"],
        "smiles": ["smiles", "gol"],
        "amex": ["amex", "american express", "membership rewards"],
        "error_fare": ["error fare", "tarifa error", "precio error"],
        "award_discount": ["desconto na emissao", "desconto em viagens com milhas", "trechos a partir", "award sale", "promo rewards"],
        "stackable": ["gift card", "shopping", "portal", "pontos por real", "avios por euro", "avios por libra", "milheiro"],
    }

    DATE_RANGE_PATTERNS = [
        # del 01/02/2026 al 31/03/2026
        r"(?:del|de)\s+(\d{1,2}[/-]\d{1,2}[/-]\d{2,4})\s+(?:al|a)\s+(\d{1,2}[/-]\d{1,2}[/-]\d{2,4})",
        # de 01-02-2026 a 31-03-2026
        r"(?:from)\s+(\d{1,2}[/-]\d{1,2}[/-]\d{2,4})\s+(?:to)\s+(\d{1,2}[/-]\d{1,2}[/-]\d{2,4})",
    ]

    DATE_END_PATTERNS = [
        # hasta 31/05/2026, valido ate 31/05/2026, valid until 31/05/2026
        r"(?:hasta|ate|até|valido ate|valida ate|valid until|until)\s+(\d{1,2}[/-]\d{1,2}[/-]\d{2,4})",
        # termina 31/05/2026, finaliza 31/05/2026
        r"(?:termina|finaliza|ends?)\s+(\d{1,2}[/-]\d{1,2}[/-]\d{2,4})",
    ]

    def __init__(self, db=None):
        """Initialize scraper. If db session provided, loads feeds from database."""
        self.feeds = {}
        self._source_map = {}  # feed_key -> source DB object (for updating stats)

        if db:
            self._load_feeds_from_db(db)

        # Fallback to hardcoded feeds if DB returned nothing
        if not self.feeds:
            self.feeds = dict(self.FALLBACK_FEEDS)

    def _load_feeds_from_db(self, db):
        """Load active RSS feed sources from database"""
        from ..models import Source
        sources = db.query(Source).filter(
            Source.source_type == "rss_feed",
            Source.is_active == True,
        ).order_by(Source.priority.desc()).all()

        for source in sources:
            # Create a safe key from the name (snake_case)
            key = re.sub(r"[^a-z0-9]+", "_", source.name.lower()).strip("_")
            self.feeds[key] = source.url
            self._source_map[key] = source

    def get_source_for_feed(self, feed_key: str):
        """Get the database Source object for a feed key (for updating stats)"""
        return self._source_map.get(feed_key)

    def fetch_feed(self, feed_url: str) -> Dict:
        """Obtener entradas de un feed RSS"""
        try:
            feed = feedparser.parse(feed_url)
            return {
                "status": "success",
                "feed_title": feed.feed.get("title", "Unknown"),
                "entries": feed.entries[:20],  # Ultimas 20 entradas
            }
        except Exception as e:
            return {
                "status": "error",
                "error": str(e),
                "entries": [],
            }

    def clean_html(self, html_content: str) -> str:
        """Limpiar contenido HTML y extraer texto"""
        if not html_content:
            return ""

        soup = BeautifulSoup(html_content, "html.parser")
        return soup.get_text(separator=" ", strip=True)

    def detect_keywords(self, text: str) -> Dict[str, List[str]]:
        """Detectar palabras clave en el texto"""
        text_lower = text.lower()
        detected = {}

        for category, keywords in self.KEYWORDS.items():
            found = [kw for kw in keywords if kw in text_lower]
            if found:
                detected[category] = found

        return detected

    def calculate_relevance_score(self, entry: Dict) -> int:
        """Calcular puntuacion de relevancia (0-100)"""
        score = 0

        # Combinar titulo y descripcion
        title = entry.get("title", "")
        summary = entry.get("summary", "")
        content = self.clean_html(summary)
        full_text = f"{title} {content}".lower()

        # Detectar keywords
        detected = self.detect_keywords(full_text)

        # Puntuacion por categoria
        if "avios" in detected:
            score += 30
        if "bonus" in detected:
            score += 25
        if "transfer" in detected:
            score += 20
        if "promo" in detected:
            score += 15
        if "livelo" in detected or "esfera" in detected:
            score += 20
        if "amex" in detected:
            score += 15
        if "error_fare" in detected:
            score += 35  # Muy relevante
        if "award_discount" in detected:
            score += 25
        if "stackable" in detected:
            score += 10

        # Bonus por multiples keywords
        if len(detected) >= 3:
            score += 10

        return min(score, 100)

    def classify_alert_type(self, detected_keywords: Dict[str, List[str]]) -> str:
        """Clasificar tipo de alerta basado en keywords"""
        if "error_fare" in detected_keywords:
            return "error_fare"
        if "bonus" in detected_keywords and "transfer" in detected_keywords:
            return "bonus_transfer"
        if "bonus" in detected_keywords and "purchase" in detected_keywords:
            return "purchase_bonus"
        if "award_discount" in detected_keywords:
            return "award_discount"
        if "promo" in detected_keywords:
            return "promo_detected"
        return "general_info"

    def determine_country(self, feed_name: str, text: str) -> str:
        """Determinar pais de la promocion usando la BD source o contenido"""
        text_lower = text.lower()

        # 1. Use country from DB source if available
        source = self._source_map.get(feed_name)
        if source:
            # If source has a specific country, use it (but check content for overrides)
            source_country = source.country
            if source_country in ("ES", "BR", "GI"):
                return source_country
            # For INT sources, try to classify by content
            if any(word in text_lower for word in ["brasil", "brazil", "livelo", "esfera", "smiles", "azul", "gol"]):
                return "BR"
            if any(word in text_lower for word in ["espana", "spain", "iberia", "vueling", "madrid"]):
                return "ES"
            return "INT"

        # 2. Fallback: classify by content only
        if any(word in text_lower for word in ["brasil", "brazilian", "brazil", "livelo", "esfera", "smiles"]):
            return "BR"
        if any(word in text_lower for word in ["espana", "spain", "iberia", "vueling"]):
            return "ES"
        if any(word in text_lower for word in ["gibraltar", "british airways", "ba executive", "avios uk"]):
            return "GI"
        return "INT"

    def _parse_date_token(self, token: str) -> Optional[datetime]:
        """Convierte dd/mm/yyyy o dd-mm-yyyy a datetime."""
        clean_token = token.strip().replace("-", "/")
        parts = clean_token.split("/")
        if len(parts) != 3:
            return None

        try:
            day = int(parts[0])
            month = int(parts[1])
            year = int(parts[2])
            if year < 100:
                year += 2000
            return datetime(year, month, day)
        except Exception:
            return None

    def extract_date_window(self, text: str) -> Tuple[Optional[datetime], Optional[datetime]]:
        """Extrae fecha inicio y fin si aparecen en el contenido."""
        text_lower = text.lower()

        for pattern in self.DATE_RANGE_PATTERNS:
            match = re.search(pattern, text_lower)
            if match:
                start_date = self._parse_date_token(match.group(1))
                end_date = self._parse_date_token(match.group(2))
                if start_date or end_date:
                    return start_date, end_date

        for pattern in self.DATE_END_PATTERNS:
            match = re.search(pattern, text_lower)
            if match:
                end_date = self._parse_date_token(match.group(1))
                if end_date:
                    return None, end_date

        return None, None

    def extract_bonus_percentage(self, text: str) -> Optional[float]:
        """Detecta bonus porcentual en texto, priorizando rangos razonables de transferencias."""
        matches = re.findall(r"([+]?\d{1,3})\s*%", text)
        if not matches:
            return None

        candidates = []
        for raw in matches:
            try:
                value = float(raw.replace("+", ""))
                if 5 <= value <= 300:
                    candidates.append(value)
            except Exception:
                continue

        if not candidates:
            return None

        return max(candidates)

    def parse_entry(self, entry: Dict, feed_name: str) -> Dict:
        """Parsear una entrada del feed"""
        title = entry.get("title", "")
        summary = entry.get("summary", "")
        link = entry.get("link", "")

        # Limpiar contenido
        content = self.clean_html(summary)
        full_text = f"{title} {content}"

        # Detectar keywords
        detected_keywords = self.detect_keywords(full_text)

        # Calcular relevancia
        relevance_score = self.calculate_relevance_score(entry)

        # Determinar tipo y pais
        alert_type = self.classify_alert_type(detected_keywords)
        country = self.determine_country(feed_name, full_text)

        # Extraer programa relacionado
        related_program = None
        text_lower = full_text.lower()
        if "avios" in detected_keywords or "iberia" in text_lower:
            related_program = "Iberia Club"
        elif "livelo" in detected_keywords:
            related_program = "Livelo"
        elif "esfera" in detected_keywords:
            related_program = "Esfera"
        elif "smiles" in detected_keywords:
            related_program = "Smiles"
        elif "amex" in detected_keywords:
            related_program = "American Express"

        # Determinar prioridad
        priority = "normal"
        if (
            ("bonus" in detected_keywords and "transfer" in detected_keywords and "purchase" in detected_keywords)
            or ("award_discount" in detected_keywords and ("bonus" in detected_keywords or "avios" in detected_keywords))
        ):
            alert_type = "stackable_combo"
            priority = "urgent"

        if relevance_score >= 90:
            priority = "urgent"
        elif relevance_score >= 70:
            priority = "high"
        elif relevance_score < 40:
            priority = "low"

        # Fecha de publicacion
        published = entry.get("published_parsed")
        pub_date = datetime(*published[:6]) if published else datetime.utcnow()

        # Metadata de promociones temporales
        start_date, end_date = self.extract_date_window(full_text)
        bonus_percentage = self.extract_bonus_percentage(full_text)
        source = self._source_map.get(feed_name)
        source_name = source.name if source else feed_name
        confidence = "official" if source and source.source_type in ("official_web", "promo_landing") else "inferred"

        # Regla especifica BR: bonus de transferencia
        if country == "BR" and bonus_percentage and related_program in ("Livelo", "Esfera", "Smiles"):
            alert_type = "bonus_transfer"
            priority = "high" if bonus_percentage < 80 else "urgent"

        return {
            "title": title,
            "message": content[:500] if len(content) > 500 else content,  # Resumen
            "alert_type": alert_type,
            "priority": priority,
            "source_url": link,
            "source_type": "rss_blog",
            "source_name": source_name,
            "related_program": related_program,
            "country": country,
            "confidence": confidence,
            "last_verified_at": datetime.utcnow(),
            "start_date": start_date,
            "end_date": end_date,
            "detected_bonus_percentage": bonus_percentage,
            "full_content": content,
            "relevance_score": relevance_score,
            "detected_keywords": detected_keywords,
            "published_date": pub_date,
        }

    def scrape_all_feeds(self, min_relevance: int = 40) -> List[Dict]:
        """Scrapear todos los feeds y retornar entradas relevantes"""
        all_entries = []

        for feed_name, feed_url in self.feeds.items():
            print(f"Scraping {feed_name}...")
            result = self.fetch_feed(feed_url)

            if result["status"] == "success":
                for entry in result["entries"]:
                    parsed = self.parse_entry(entry, feed_name)

                    # Filtrar por relevancia
                    if parsed["relevance_score"] >= min_relevance:
                        parsed["source_feed"] = feed_name
                        all_entries.append(parsed)

        # Ordenar por relevancia (mayor a menor)
        all_entries.sort(key=lambda x: x["relevance_score"], reverse=True)

        return all_entries

    def scrape_feed_by_name(self, feed_name: str, min_relevance: int = 30) -> List[Dict]:
        """Scrapear un feed especifico"""
        if feed_name not in self.feeds:
            return []

        feed_url = self.feeds[feed_name]
        result = self.fetch_feed(feed_url)

        entries = []
        if result["status"] == "success":
            for entry in result["entries"]:
                parsed = self.parse_entry(entry, feed_name)
                if parsed["relevance_score"] >= min_relevance:
                    parsed["source_feed"] = feed_name
                    entries.append(parsed)

        entries.sort(key=lambda x: x["relevance_score"], reverse=True)
        return entries
