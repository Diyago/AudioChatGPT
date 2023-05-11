AI_ROLE_OPTIONS_EN: list[str] = [
    "helpful assistant",
    "code assistant",
    "code reviewer",
    "text improver",
    "cinema expert",
    "sport expert",
    "online games expert",
    "food recipes expert",
    "English grammar expert",
    "friendly and helpful teaching assistant",
    "laconic assistant",
    "helpful, pattern-following assistant",
    "translate corporate jargon into plain English",
]

AI_ROLE_OPTIONS_RU: list[str] = [
    "ассистент, который готов помочь",
    "ассистент программиста",
    "рецензент кода программиста",
    "эксперт по улучшению текста",
    "эксперт по кинематографу",
    "эксперт в области спорта",
    "эксперт в онлайн-играх",
    "эксперт по рецептам блюд",
    "эксперт по английской грамматике",
    "эксперт по русской грамматике",
    "дружелюбный и полезный помощник преподавателя",
    "лаконичный помощник",
    "полезный помощник, следующий шаблонам",
    "переводчик корпоративного жаргона на простой русский",
]

HEADER_STYLES = {
    "container": {
        "padding": "0px",
        "display": "grid",
        "margin": "0!important",
        "background-color": "#2C3333"
    },
    "icon": {"color": "#CBE4DE", "font-size": "14px"},
    "nav-link": {
        "font-size": "14px",
        "text-align": "center",
        "margin": "auto",
        "background-color": "#2C3333",
        "height": "30px",
        "width": "7rem",
        "color": "#CBE4DE",
        "border-radius": "5px"
    },
    "nav-link-selected": {
        "background-color": "#2E4F4F",
        "font-weight": "300",
        "color": "#f5f5f5",
        "border": "1px solid #0E8388"
    }
}
REPO_URL: str = "https://github.com/Diyago/AudioChatGPT"
README_URL: str = f"{REPO_URL}#readme"
BUG_REPORT_URL: str = f"{REPO_URL}/issues"
AI_TALKS_URL: str = "https://demo.streamlit.app/"
