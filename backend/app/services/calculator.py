"""
Servicio de cálculo de conversión de puntos
"""
from typing import Dict, List, Optional
from sqlalchemy.orm import Session
from ..models import LoyaltyProgram


class PointsCalculator:
    """Calculadora de conversión de puntos/millas/avios"""

    def __init__(self, db: Session):
        self.db = db

    def convert_to_avios(self, program_id: int, points: float) -> Optional[Dict]:
        """
        Convierte puntos de un programa a Avios

        Args:
            program_id: ID del programa origen
            points: Cantidad de puntos a convertir

        Returns:
            Diccionario con el resultado de la conversión o None si no es convertible
        """
        program = self.db.query(LoyaltyProgram).filter(LoyaltyProgram.id == program_id).first()

        if not program:
            return None

        if program.avios_ratio is None:
            return {
                "program_name": program.name,
                "program_currency": program.currency,
                "input_points": points,
                "avios_ratio": None,
                "avios_output": None,
                "convertible": False,
                "message": f"{program.name} no tiene conversión directa a Avios"
            }

        avios_output = points / program.avios_ratio

        return {
            "program_name": program.name,
            "program_currency": program.currency,
            "input_points": points,
            "avios_ratio": program.avios_ratio,
            "avios_output": avios_output,
            "convertible": True,
            "message": f"{points:,.0f} {program.currency} = {avios_output:,.0f} Avios (ratio {program.avios_ratio}:1)"
        }

    def convert_between_programs(
        self,
        source_program_id: int,
        target_program_id: int,
        points: float,
        bonus_percentage: float = 0.0
    ) -> Optional[Dict]:
        """
        Convierte puntos entre dos programas (via Avios como puente)

        Args:
            source_program_id: ID del programa origen
            target_program_id: ID del programa destino
            points: Cantidad de puntos a convertir
            bonus_percentage: Bonus de transferencia (e.g., 50 para 50%)

        Returns:
            Diccionario con el resultado de la conversión
        """
        source = self.db.query(LoyaltyProgram).filter(LoyaltyProgram.id == source_program_id).first()
        target = self.db.query(LoyaltyProgram).filter(LoyaltyProgram.id == target_program_id).first()

        if not source or not target:
            return None

        # Convertir source a Avios
        if source.avios_ratio is None:
            return {
                "error": f"{source.name} no es convertible a Avios"
            }

        avios_intermediate = points / source.avios_ratio

        # Aplicar bonus
        if bonus_percentage > 0:
            avios_intermediate = avios_intermediate * (1 + bonus_percentage / 100)

        # Convertir de Avios a target
        if target.avios_ratio is None:
            return {
                "error": f"Avios no es convertible a {target.name}"
            }

        target_points = avios_intermediate * target.avios_ratio

        effective_ratio = target_points / points if points > 0 else 0

        return {
            "source_program": source.name,
            "source_currency": source.currency,
            "target_program": target.name,
            "target_currency": target.currency,
            "input_points": points,
            "output_points": target_points,
            "avios_intermediate": avios_intermediate,
            "bonus_percentage": bonus_percentage,
            "base_ratio": f"{source.avios_ratio}:1 → 1:{target.avios_ratio}",
            "effective_ratio": effective_ratio,
            "message": f"{points:,.0f} {source.currency} = {target_points:,.0f} {target.currency}" +
                      (f" (con {bonus_percentage}% bonus)" if bonus_percentage > 0 else "")
        }

    def get_all_conversions_to_avios(self, points: float) -> List[Dict]:
        """
        Calcula la conversión a Avios para todos los programas convertibles

        Args:
            points: Cantidad de puntos a convertir

        Returns:
            Lista de conversiones ordenadas por mejor valor
        """
        programs = self.db.query(LoyaltyProgram).filter(LoyaltyProgram.avios_ratio.isnot(None)).all()

        conversions = []
        for program in programs:
            conversion = self.convert_to_avios(program.id, points)
            if conversion and conversion["convertible"]:
                conversions.append(conversion)

        # Ordenar por cantidad de Avios obtenidos (mayor a menor)
        conversions.sort(key=lambda x: x["avios_output"], reverse=True)

        return conversions

    def compare_value(self, points_dict: Dict[int, float]) -> List[Dict]:
        """
        Compara el valor en Avios de diferentes cantidades de puntos

        Args:
            points_dict: Diccionario {program_id: points}

        Returns:
            Lista de comparaciones ordenadas por valor en Avios
        """
        results = []

        for program_id, points in points_dict.items():
            conversion = self.convert_to_avios(program_id, points)
            if conversion and conversion["convertible"]:
                results.append(conversion)

        # Ordenar por cantidad de Avios (mayor a menor)
        results.sort(key=lambda x: x["avios_output"], reverse=True)

        return results
