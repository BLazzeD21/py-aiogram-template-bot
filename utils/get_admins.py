from config_data.config import Config, load_config

def get_admin_ids() -> list:    
    configuration: Config = load_config(".env")
    return configuration.tg_bot.admin_ids