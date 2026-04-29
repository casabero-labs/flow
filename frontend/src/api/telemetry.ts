import api from './client';

export interface TelemetryEvent {
  event_type: string;
  event_data?: Record<string, unknown>;
  session_id?: string;
}

/**
 * Genera o recupera un session_id persistente en sessionStorage.
 */
export function getSessionId(): string {
  let sid = sessionStorage.getItem('flow_session_id');
  if (!sid) {
    sid = crypto.randomUUID();
    sessionStorage.setItem('flow_session_id', sid);
  }
  return sid;
}

/**
 * Envía un evento de telemetría al backend.
 * No hace throw en error — falla silenciosamente.
 */
export async function sendTelemetryEvent(
  event_type: string,
  event_data?: Record<string, unknown>,
): Promise<void> {
  try {
    const session_id = getSessionId();
    await api.post('/telemetry/', {
      event_type,
      event_data: event_data ?? {},
      session_id,
    });
  } catch {
    // Telemetría no debe interrumpir la app
  }
}
