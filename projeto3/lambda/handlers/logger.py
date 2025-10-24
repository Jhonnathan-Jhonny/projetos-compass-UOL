import logging

#Cofnigurçação do logger
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def log_process(event):
    logger.info("Processo iniciado às %s", event.get("timestamp", "sem data"))

    received_data = event.get("data", {"data": "placeholder"})
    logger.info("Dados recebidos: %s", received_data)

    output = {"result": "placeholder_output"}
    logger.info("Output processado: %s", output)

    final_json = {"status": "success", "data": "placeholder"}
    logger.info("JSON final: %s", final_json)

    try:
        raise ValueError("Erro simulado")
    except Exception as e:
        logger.error("Erro ocorrido: %s", str(e), exc_info=True)

if __name__ == "__main__":
    test_event = {"timestamp": "04:23 AM -03 11/08/2025", "data": "teste"}
    log_process(test_event)