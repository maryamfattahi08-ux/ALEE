from backend.models import ExternalDiagnosticResult


diagnostic_records: list[ExternalDiagnosticResult] = []


def save_diagnostic_result(
    result: ExternalDiagnosticResult
) -> ExternalDiagnosticResult:

    diagnostic_records.append(result)

    return result


def get_latest_diagnostic_result():
    
    if not diagnostic_records:
        return None

    return diagnostic_records[-1]