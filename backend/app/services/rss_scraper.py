"""
Scraper de feeds RSS de blogs de viajes y puntos
"""
import feedparser
from bs4 import BeautifulSoup
from typing import List, Dict
from datetime import datetime
import re


class RSSFeedScraper:
    """Scraper de feeds RSS de blogs de viajes"""

    # Feeds de blogs españoles
    SPANISH_FEEDS = {
        "puntos_viajeros": "https://puntosviajeros.com/feed/",
        "travel_dealz": "https://travel-dealz.com/feed/",
    }

    # Feeds de blogs UK/Gibraltar (relevantes para fronterizos y Avios)
    UK_GIBRALTAR_FEEDS = {
        "head_for_points": "https://www.headforpoints.com/feed/",  # Principal UK
        "insideflyer_uk": "https://www.insideflyer.co.uk/feed/",
        "turning_left_less": "https://www.turningleftforless.com/feed/",
    }

    # Feeds internacionales (relevantes para todos)
    INTERNATIONAL_FEEDS = {
        "one_mile_time": "https://onemileatatime.com/feed/",
        "the_points_guy": "https://thepointsguy.com/feed/",
        "frequent_miler": "https://frequentmiler.com/feed/",
    }

    # Feeds de blogs brasileños
    BRAZILIAN_FEEDS = {
        "melhores_destinos": "https://www.melhoresdestinos.com.br/feed",
        "passageiro_primeira": "https://passageirodeprimeira.com/feed/",
        "pontos_voar": "https://pontospravoar.com/feed/",
        "mil_milhas": "https://www.milmilhas.com.br/blog/feed/",
        "blog_maxmilhas": "https://blog.maxmilhas.com.br/feed/",
    }

    # Palabras clave para detectar promociones relevantes
    KEYWORDS = {
        "bonus": ["bonus", "bónus", "bonificación", "bonificacao"],
        "avios": ["avios", "iberia", "british airways", "ba", "vueling"],
        "transfer": ["transferencia", "transferência", "transfer", "conversão", "conversión"],
        "purchase": ["compra", "buy", "comprar"],
        "promo": ["promoción", "promoção", "promo", "oferta", "deal"],
        "livelo": ["livelo"],
        "esfera": ["esfera"],
        "smiles": ["smiles", "gol"],
        "amex": ["amex", "american express", "membership rewards"],
        "error_fare": ["error fare", "tarifa error", "precio error"],
    }

    def __init__(self):
        self.feeds = {
            **self.SPANISH_FEEDS,
            **self.UK_GIBRALTAR_FEEDS,
            **self.INTERNATIONAL_FEEDS,
            **self.BRAZILIAN_FEEDS
        }

    def fetch_feed(self, feed_url: str) -> Dict:
        """Obtener entradas de un feed RSS"""
        try:
            feed = feedparser.parse(feed_url)
            return {
                "status": "success",
                "feed_title": feed.feed.get("title", "Unknown"),
                "entries": feed.entries[:20]  # Últimas 20 entradas
            }
        except Exception as e:
            return {
                "status": "error",
                "error": str(e),
                "entries": []
            }

    def clean_html(self, html_content: str) -> str:
        """Limpiar contenido HTML y extraer texto"""
        if not html_content:
            return ""

        soup = BeautifulSoup(html_content, 'html.parser')
        return soup.get_text(separator=' ', strip=True)

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
        """Calcular puntuación de relevancia (0-100)"""
        score = 0

        # Combinar título y descripción
        title = entry.get("title", "")
        summary = entry.get("summary", "")
        content = self.clean_html(summary)
        full_text = f"{title} {content}".lower()

        # Detectar keywords
        detected = self.detect_keywords(full_text)

        # Puntuación por categoría
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

        # Bonus por múltiples keywords
        if len(detected) >= 3:
            score += 10

        return min(score, 100)

    def classify_alert_type(self, detected_keywords: Dict[str, List[str]]) -> str:
        """Clasificar tipo de alerta basado en keywords"""
        if "error_fare" in detected_keywords:
            return "error_fare"
        elif "bonus" in detected_keywords and "transfer" in detected_keywords:
            return "bonus_transfer"
        elif "bonus" in detected_keywords and "purchase" in detected_keywords:
            return "purchase_bonus"
        elif "promo" in detected_keywords:
            return "promo_detected"
        else:
            return "general_info"

    def determine_country(self, feed_name: str, text: str) -> str:
        """Determinar país de la promoción"""
        text_lower = text.lower()

        # Por feed
        if feed_name in self.BRAZILIAN_FEEDS:
            return "BR"
        elif feed_name in self.SPANISH_FEEDS:
            return "ES"
        elif feed_name in self.UK_GIBRALTAR_FEEDS:
            # UK/Gibraltar - verificar si es específico de España por contenido
            if any(word in text_lower for word in ["spain", "españa", "iberia", "madrid", "barcelona"]):
                return "ES"
            return "INT"  # UK/Gibraltar va a INT por defecto
        elif feed_name in self.INTERNATIONAL_FEEDS:
            # Clasificar por contenido
            if any(word in text_lower for word in ["brasil", "brazil", "livelo", "esfera", "smiles", "azul", "gol"]):
                return "BR"
            elif any(word in text_lower for word in ["españa", "spain", "iberia", "vueling", "madrid"]):
                return "ES"
            return "INT"

        # Por contenido (fallback)
        if any(word in text_lower for word in ["brasil", "brazilian", "brazil", "livelo", "esfera", "smiles"]):
            return "BR"
        elif any(word in text_lower for word in ["españa", "spain", "iberia", "vueling"]):
            return "ES"
        elif any(word in text_lower for word in ["gibraltar", "british airways", "ba executive", "avios uk"]):
            return "GI"
        else:
            return "INT"

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

        # Determinar tipo y país
        alert_type = self.classify_alert_type(detected_keywords)
        country = self.determine_country(feed_name, full_text)

        # Extraer programa relacionado
        related_program = None
        if "avios" in detected_keywords or "iberia" in full_text.lower():
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
        if relevance_score >= 70:
            priority = "high"
        elif relevance_score >= 90:
            priority = "urgent"
        elif relevance_score < 40:
            priority = "low"

        # Fecha de publicación
        published = entry.get("published_parsed")
        pub_date = datetime(*published[:6]) if published else datetime.utcnow()

        return {
            "title": title,
            "message": content[:500] if len(content) > 500 else content,  # Resumen
            "alert_type": alert_type,
            "priority": priority,
            "source_url": link,
            "source_type": "rss_blog",
            "source_name": feed_name,
            "related_program": related_program,
            "country": country,
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
        """Scrapear un feed específico"""
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
