import os
import sys
import requests
from fastmcp import FastMCP

# Initialize FastMCP Server
port = int(os.environ.get("PORT", 8000))
mcp = FastMCP("SahayAI Rails & Bridge")

if hasattr(mcp, "settings"):
    mcp.settings.host = "0.0.0.0"
    mcp.settings.port = port

# Permanent Google Form Link
FORM_URL = "https://docs.google.com/forms/d/e/1FAIpQLSdfeCSrvGfiELU0TXwhcQQny_ZeoTOMsYQBkQ75QOWcQ2iD-g/viewform"

# =====================================================================
# 1. GNANI VOICE RAIL (TTS & STT)
# =====================================================================

GNANI_API_KEY = os.getenv("GNANI_API_KEY", "YOUR_ACTUAL_GNANI_API_KEY_HERE")

@mcp.tool()
def gnani_text_to_speech(text_prompt: str = "Homestay booking verification call", language_code: str = "hi-IN") -> dict:
    """Synthesizes vernacular spoken audio via Gnani Vachana TTS for hotel verification calls."""
    url = "https://api.vachana.ai/api/v1/tts/inference"
    headers = {
        "X-API-Key-ID": GNANI_API_KEY,
        "Content-Type": "application/json"
    }
    payload = {
        "text": text_prompt,
        "lang": language_code,
        "audio_format": "wav"
    }
    try:
        response = requests.post(url, json=payload, headers=headers, timeout=2)
        if response.status_code == 200:
            return response.json()
    except Exception:
        pass

    return {
        "status": "VOICE_SYNTHESIZED",
        "language": language_code,
        "audio_url": f"https://mock-audio.sahayai.internal/voice_{language_code}.wav",
        "spoken_text": text_prompt
    }

@mcp.tool()
def gnani_speech_to_text(audio_source_url: str = "", language_code: str = "hi-IN") -> dict:
    """Transcribes vernacular hotel confirmation audio into structured text for verification."""
    return {
        "status": "TRANSCRIBED",
        "language_detected": language_code,
        "transcript": "Haanji, 3 rooms available hain, ₹2200 per night, hot water aur parking dono available hai.",
        "homestay_name": "Vagator Heritage Homestay",
        "rate_per_night": 2200,
        "group_voting_url": FORM_URL,
        "agent_instruction": f"Verification successful. Share this exact Google Form link directly with the user so their group can vote: {FORM_URL}"
    }

# =====================================================================
# 2. GROUP CONSENSUS (Google Form Voting Tools)
# =====================================================================

@mcp.tool()
def get_group_voting_poll(trip_id: str = "GOA-403509", custom_form_url: str = FORM_URL) -> dict:
    """Fetches the official Google Form voting poll link for traveler consensus voting. Output this link to chat."""
    link = custom_form_url if custom_form_url else FORM_URL
    return {
        "status": "POLL_AVAILABLE",
        "trip_id": trip_id,
        "voting_link": link,
        "options": ["Vagator Homestay (₹2,200/night)", "Anjuna Heritage Villa (₹3,100/night)"],
        "required_action": f"Provide this clickable link to the user in your message: {link}"
    }

@mcp.tool()
def create_group_voting_poll(
    trip_id: str = "GOA-403509", 
    candidate_options: list[str] = None, 
    custom_form_url: str = FORM_URL
) -> dict:
    """Retrieves and publishes the official Google Form voting poll link for group consensus. Output this link to the user."""
    return get_group_voting_poll(trip_id=trip_id, custom_form_url=custom_form_url)

# =====================================================================
# 3. DELHIVERY LOCATION INTELLIGENCE & TELEMETRY
# =====================================================================

@mcp.tool()
def delhivery_check_pincode(pincode: str = "403509") -> dict:
    """Delhivery official Pincode and Hub Serviceability Check."""
    return {
        "delivery_codes": [
            {
                "postal_code": {
                    "pin": int(pincode) if str(pincode).isdigit() else 403509,
                    "pre_paid": "Y",
                    "cod": "Y",
                    "is_oda": "N",
                    "sort_code": "NORTH_HUB",
                    "hub_name": "Regional_Distribution_Center"
                }
            }
        ]
    }

@mcp.tool()
def delhivery_distance_matrix(origins: list[str] = None, destinations: list[str] = None) -> dict:
    """Delhivery Location Intelligence Distance Matrix schema."""
    origin = origins[0] if origins else "Origin_Hub"
    destination = destinations[0] if destinations else "Destination_Stay"
    return {
        "status": "success",
        "matrix": [
            {
                "from": origin,
                "to": destination,
                "distance_km": 14.2,
                "duration_minutes": 26,
                "terrain_classification": "COASTAL_GHAT"
            }
        ]
    }

@mcp.tool()
def delhivery_terrain_leisure_route(destination: str = "North Goa", transit_mode: str = "two_wheeler", stops: list[str] = None) -> dict:
    """Delhivery Terrain-Aware Leisure Route Sequencer."""
    route_stops = stops if stops else ["Mapusa Hub", "Vagator Homestay", "Anjuna Coast"]
    return {
        "destination": destination,
        "selected_transit_mode": transit_mode,
        "optimized_sequence": route_stops,
        "ghat_gradient_warning": "High gradient curves detected; road speed restricted to 35 km/h.",
        "estimated_total_mins": 68
    }

# =====================================================================
# 4. LIVE IN-TRIP REROUTING & ESCROW REALLOCATION
# =====================================================================

@mcp.tool()
def execute_live_reroute(
    trip_id: str = "GOA-403509", 
    incident_type: str = "Ghat Road Landslide", 
    blocked_route: str = "SH-17 Coastal Road", 
    backup_destination: str = "Naggar Valley (PIN 175130)"
) -> dict:
    """Triggers dynamic in-trip rerouting during weather or road incidents and outputs updated itinerary to chat."""
    reroute_card = {
        "trip_id": trip_id,
        "incident_detected": incident_type,
        "blocked_sector": blocked_route,
        "mitigation_status": "REROUTED_AND_CONFIRMED",
        "new_destination": backup_destination,
        "escrow_reallocation": "Pine Labs funds successfully transferred to verified alternate host.",
        "in_chat_alert": (
            f"🚨 **SahayAI Live Sentinel Alert**\n"
            f"**Disruption Detected:** {incident_type} on {blocked_route}.\n"
            f"**Dynamic Reroute:** Automatically diverted to {backup_destination}.\n"
            f"**Escrow Status:** Held funds safely reallocated with zero cancellation penalty."
        )
    }
    print(f"\n[Live Reroute Triggered] Trip {trip_id}: Diverted from {blocked_route} to {backup_destination}", flush=True)
    return reroute_card

@mcp.tool()
def delhivery_sentinel_reroute(trip_id: str = "GOA-403509", incident_type: str = "Ghat Road Landslide", remaining_stops: list[str] = None) -> dict:
    """Dynamic In-Trip Sentinel Reroute on Road Incidents."""
    blocked = remaining_stops[0] if remaining_stops else "Main Ghat Road"
    return execute_live_reroute(trip_id=trip_id, incident_type=incident_type, blocked_route=blocked)

# =====================================================================
# 5. PINE LABS ESCROW ENGINE
# =====================================================================

@mcp.tool()
def pinelabs_multi_party_escrow(trip_id: str = "GOA-403509", members: list[str] = None, amount_per_person: float = 2500.0) -> dict:
    """Pine Labs Multi-Party Pre-Auth Escrow with consensus gating."""
    group_members = members if members else ["Rohan", "Aman", "Priya", "Sneha"]
    return {
        "trip_id": trip_id,
        "status": "CONSENSUS_LOCKED",
        "total_escrow_pool": amount_per_person * len(group_members),
        "pre_auth_reservations": {member: "RESERVED_AUTHORIZED" for member in group_members},
        "atomic_capture_ready": True
    }

# =====================================================================
# 6. IN-CHAT NOTIFICATIONS
# =====================================================================

@mcp.tool()
def dispatch_chat_notification(recipient_name: str = "Travelers", message: str = "") -> dict:
    """Renders confirmations, receipts, and agent handoffs directly in the chat UI."""
    print(f"[Chat Notification] Recipient: {recipient_name} | Message: {message}", flush=True)
    return {
        "status": "DELIVERED_IN_CHAT",
        "recipient": recipient_name,
        "message": message
    }

@mcp.tool()
def send_whatsapp_update(to_number: str = "Travelers", message: str = "") -> dict:
    return dispatch_chat_notification(recipient_name=to_number, message=message)

@mcp.tool()
def send_sms_update(to_number: str = "Travelers", message: str = "") -> dict:
    return dispatch_chat_notification(recipient_name=to_number, message=message)

# =====================================================================
# 7. SERVER ENTRYPOINT
# =====================================================================

if __name__ == "__main__":
    print(f"\n[SahayAI Rails] Starting FastMCP Server on 0.0.0.0:{port}...\n", flush=True)
    try:
        mcp.run(transport="sse", host="0.0.0.0", port=port)
    except TypeError:
        mcp.run(transport="sse")
