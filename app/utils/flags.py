# app/utils/flags.py

FLAGS: dict[str, str] = {
    "FR": "🇫🇷", "MA": "🇲🇦", "US": "🇺🇸", "GB": "🇬🇧", "DE": "🇩🇪",
    "ES": "🇪🇸", "IT": "🇮🇹", "PT": "🇵🇹", "NL": "🇳🇱", "BE": "🇧🇪",
    "BR": "🇧🇷", "AR": "🇦🇷", "JP": "🇯🇵", "CN": "🇨🇳", "IN": "🇮🇳",
    "CA": "🇨🇦", "SA": "🇸🇦", "AE": "🇦🇪", "TR": "🇹🇷", "SE": "🇸🇪",
    "DK": "🇩🇰", "NO": "🇳🇴", "CH": "🇨🇭", "PL": "🇵🇱", "HR": "🇭🇷",
}

TEAM_TO_ISO2: dict[str, str] = {
    # Clubs (exemples; complète selon tes besoins)
    "Paris Saint-Germain": "FR",
    "Olympique de Marseille": "FR",
    "AS Monaco": "FR",
    "Real Madrid": "ES",
    "FC Barcelona": "ES",
    "Atlético de Madrid": "ES",
    "Manchester City": "GB",
    "Manchester United": "GB",
    "Liverpool": "GB",
    "Arsenal": "GB",
    "Bayern Munich": "DE",
    "Borussia Dortmund": "DE",
    "Juventus": "IT",
    "Inter": "IT",
    "AC Milan": "IT",
    "Benfica": "PT",
    "FC Porto": "PT",
    "Ajax": "NL",
    "France": "FR",
    "Morocco": "MA",
    "United States": "US",
    "England": "GB",
    "Germany": "DE",
    "Spain": "ES",
    "Italy": "IT",
    "Brazil": "BR",
    "Argentina": "AR",
    "Japan": "JP",
    "Netherlands": "NL",
    "Colombia": "CO",

}

def iso2_for_team(team_name: str) -> str | None:
    iso = TEAM_TO_ISO2.get(team_name)
    return iso.lower() if iso else None
