"""
Scheduler para tareas automáticas con APScheduler
"""
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger
from .database import SessionLocal
from .services.promotion_manager import PromotionManager
import logging

logger = logging.getLogger(__name__)


def scan_promotions_job():
    """Job para escanear promociones automáticamente"""
    db = SessionLocal()
    try:
        logger.info("Iniciando escaneo automático de promociones...")
        manager = PromotionManager(db)
        result = manager.scan_and_save_promotions(min_relevance=50)

        logger.info(
            f"Escaneo completado: {result['new_alerts']} nuevas, "
            f"{result['duplicates']} duplicadas, {result['errors']} errores"
        )
    except Exception as e:
        logger.error(f"Error en escaneo automático: {e}")
    finally:
        db.close()


# Crear scheduler
scheduler = BackgroundScheduler()


def start_scheduler():
    """Iniciar el scheduler con las tareas programadas"""

    # Escanear promociones cada 2 horas
    scheduler.add_job(
        scan_promotions_job,
        trigger=CronTrigger(minute=0, hour="*/2"),  # Cada 2 horas en punto
        id="scan_promotions",
        name="Escanear promociones de blogs RSS",
        replace_existing=True
    )

    # También puedes añadir un job inmediato al arrancar (opcional)
    # scheduler.add_job(scan_promotions_job, 'date', run_date=datetime.now() + timedelta(seconds=30))

    scheduler.start()
    logger.info("Scheduler iniciado - Escaneará promociones cada 2 horas")


def stop_scheduler():
    """Detener el scheduler"""
    if scheduler.running:
        scheduler.shutdown()
        logger.info("Scheduler detenido")
