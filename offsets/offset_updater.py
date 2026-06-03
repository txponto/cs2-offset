import os
import json
import requests

urls = {
    "info": "https://github.com/a2x/cs2-dumper/raw/refs/heads/main/output/info.json",
    "offsets": "https://github.com/a2x/cs2-dumper/raw/refs/heads/main/output/offsets.json",
    "client_dll": "https://github.com/a2x/cs2-dumper/raw/refs/heads/main/output/client_dll.json",
}


def get_build_number():
    response = requests.get(urls["info"], timeout=15)
    response.raise_for_status()
    game_info = response.json()
    return int(game_info.get("build_number", 0))


def get_raw_file(url):
    response = requests.get(url, timeout=15)
    response.raise_for_status()
    return response.json()


def get_path():
    if os.path.isfile("./offsets/offsets.json"):
        return "./offsets/offsets.json"
    elif os.path.isfile("./offsets.json"):
        return "./offsets.json"
    return None


def get_field(classes, class_name, field_name):
    try:
        return classes[class_name]["fields"][field_name]
    except KeyError as exc:
        raise KeyError(f"Missing schema field: {class_name}.{field_name}") from exc
    

def load_local_offsets(path):
    with open(path, "r", encoding="utf-8") as dest_file:
        return json.load(dest_file)


def save_local_offsets(path, data):
    with open(path, "w", encoding="utf-8") as dest_file:
        json.dump(data, dest_file, indent=4)
        dest_file.write("\n")


def build_updated_offsets(offsets_json, build_number, offsets, client):
    client_json_base = client["client.dll"]["classes"]

    # Core offsets
    offsets_json["build_number"] = int(build_number)

    offsets_json["dwBuildNumber"] = offsets["engine2.dll"]["dwBuildNumber"]
    offsets_json["dwLocalPlayer"] = offsets["client.dll"]["dwLocalPlayerPawn"]
    offsets_json["dwLocalPlayerController"] = offsets["client.dll"]["dwLocalPlayerController"]
    offsets_json["dwEntityList"] = offsets["client.dll"]["dwEntityList"]
    offsets_json["dwViewMatrix"] = offsets["client.dll"]["dwViewMatrix"]
    offsets_json["dwPlantedC4"] = offsets["client.dll"]["dwPlantedC4"]
    offsets_json["dwGameRules"] = offsets["client.dll"]["dwGameRules"]

    # Player / entity fields
    offsets_json["m_bIsDefusing"] = client_json_base["C_CSPlayerPawn"]["fields"]["m_bIsDefusing"]
    offsets_json["m_ArmorValue"] = client_json_base["C_CSPlayerPawn"]["fields"]["m_ArmorValue"]
    offsets_json["m_pWeaponServices"] = client_json_base["C_BasePlayerPawn"]["fields"]["m_pWeaponServices"]
    offsets_json["m_hActiveWeapon"] = client_json_base["CPlayer_WeaponServices"]["fields"]["m_hActiveWeapon"]
    offsets_json["m_bIsScoped"] = client_json_base["C_CSPlayerPawn"]["fields"]["m_bIsScoped"]

    offsets_json["m_flFlashOverlayAlpha"] = client_json_base["C_CSPlayerPawnBase"]["fields"]["m_flFlashOverlayAlpha"]

    offsets_json["m_flC4Blow"] = client_json_base["C_PlantedC4"]["fields"]["m_flC4Blow"]
    offsets_json["m_flNextBeep"] = client_json_base["C_PlantedC4"]["fields"]["m_flNextBeep"]
    offsets_json["m_flTimerLength"] = client_json_base["C_PlantedC4"]["fields"]["m_flTimerLength"]

    offsets_json["m_hPlayerPawn"] = client_json_base["CCSPlayerController"]["fields"]["m_hPlayerPawn"]
    offsets_json["m_hObserverPawn"] = client_json_base["CCSPlayerController"]["fields"]["m_hObserverPawn"]
    offsets_json["m_bPawnIsAlive"] = client_json_base["CCSPlayerController"]["fields"]["m_bPawnIsAlive"]
    offsets_json["m_iAccount"] = client_json_base["CCSPlayerController_InGameMoneyServices"]["fields"]["m_iAccount"]
    offsets_json["m_pInGameMoneyServices"] = client_json_base["CCSPlayerController"]["fields"]["m_pInGameMoneyServices"]

    offsets_json["m_sSanitizedPlayerName"] = client_json_base["CCSPlayerController"]["fields"]["m_sSanitizedPlayerName"]
    offsets_json["m_hController"] = client_json_base["C_BasePlayerPawn"]["fields"]["m_hController"]
    offsets_json["m_iszPlayerName"] = client_json_base["CBasePlayerController"]["fields"]["m_iszPlayerName"]

    offsets_json["m_iHealth"] = client_json_base["C_BaseEntity"]["fields"]["m_iHealth"]
    offsets_json["m_iTeamNum"] = client_json_base["C_BaseEntity"]["fields"]["m_iTeamNum"]
    offsets_json["m_pGameSceneNode"] = client_json_base["C_BaseEntity"]["fields"]["m_pGameSceneNode"]

    offsets_json["m_szName"] = client_json_base["CCSWeaponBaseVData"]["fields"]["m_szName"]
    offsets_json["m_vOldOrigin"] = client_json_base["C_BasePlayerPawn"]["fields"]["m_vOldOrigin"]
    offsets_json["m_vecAbsOrigin"] = client_json_base["CGameSceneNode"]["fields"]["m_vecAbsOrigin"]

    # Spectator offsets
    offsets_json["m_pObserverServices"] = client_json_base["C_BasePlayerPawn"]["fields"]["m_pObserverServices"]
    offsets_json["m_iObserverMode"] = client_json_base["CPlayer_ObserverServices"]["fields"]["m_iObserverMode"]
    offsets_json["m_hObserverTarget"] = client_json_base["CPlayer_ObserverServices"]["fields"]["m_hObserverTarget"]

    # Game rules offsets
    offsets_json["m_pGameRules"] = client_json_base["C_CSGameRulesProxy"]["fields"]["m_pGameRules"]
    offsets_json["m_nRoundStartCount"] = client_json_base["C_CSGameRules"]["fields"]["m_nRoundStartCount"]

    # Helpers
    f = lambda class_name, field_name: get_field(client_json_base, class_name, field_name)

    # ------------------------------------------------------------------
    # Player loadout / current weapons
    # ------------------------------------------------------------------
    # Pawn -> weapon services -> current carried weapon handles.
    offsets_json["m_pWeaponServices"] = f("C_BasePlayerPawn", "m_pWeaponServices")
    offsets_json["m_hMyWeapons"] = f("CPlayer_WeaponServices", "m_hMyWeapons")
    offsets_json["m_hActiveWeapon"] = f("CPlayer_WeaponServices", "m_hActiveWeapon")
    offsets_json["m_hLastWeapon"] = f("CPlayer_WeaponServices", "m_hLastWeapon")
    offsets_json["m_iAmmo"] = f("CPlayer_WeaponServices", "m_iAmmo")

    # Weapon entity ammo / clip info.
    offsets_json["m_iClip1"] = f("C_BasePlayerWeapon", "m_iClip1")
    offsets_json["m_iClip2"] = f("C_BasePlayerWeapon", "m_iClip2")
    offsets_json["m_pReserveAmmo"] = f("C_BasePlayerWeapon", "m_pReserveAmmo")

    # Econ item identity for resolving weapon/loadout item definitions.
    offsets_json["m_AttributeManager"] = f("C_EconEntity", "m_AttributeManager")
    offsets_json["m_Item"] = f("C_AttributeContainer", "m_Item")
    offsets_json["m_iItemDefinitionIndex"] = f("C_EconItemView", "m_iItemDefinitionIndex")

    # Controller-side networked loadout.
    offsets_json["m_pInventoryServices"] = f("CCSPlayerController", "m_pInventoryServices")
    offsets_json["m_vecNetworkableLoadout"] = f(
        "CCSPlayerController_InventoryServices",
        "m_vecNetworkableLoadout",
    )
    offsets_json["m_vecServerAuthoritativeWeaponSlots"] = f(
        "CCSPlayerController_InventoryServices",
        "m_vecServerAuthoritativeWeaponSlots",
    )

    # Fields inside CCSPlayerController_InventoryServices::NetworkedLoadoutSlot_t
    offsets_json["NetworkedLoadoutSlot_pItem"] = f(
        "CCSPlayerController_InventoryServices::NetworkedLoadoutSlot_t",
        "pItem",
    )
    offsets_json["NetworkedLoadoutSlot_team"] = f(
        "CCSPlayerController_InventoryServices::NetworkedLoadoutSlot_t",
        "team",
    )
    offsets_json["NetworkedLoadoutSlot_slot"] = f(
        "CCSPlayerController_InventoryServices::NetworkedLoadoutSlot_t",
        "slot",
    )

    # ------------------------------------------------------------------
    # FOV / camera services
    # ------------------------------------------------------------------
    # Pawn -> camera services -> current FOV values.
    offsets_json["m_pCameraServices"] = f("C_BasePlayerPawn", "m_pCameraServices")
    offsets_json["m_iFOV"] = f("CCSPlayerBase_CameraServices", "m_iFOV")
    offsets_json["m_iFOVStart"] = f("CCSPlayerBase_CameraServices", "m_iFOVStart")
    offsets_json["m_flFOVTime"] = f("CCSPlayerBase_CameraServices", "m_flFOVTime")
    offsets_json["m_flFOVRate"] = f("CCSPlayerBase_CameraServices", "m_flFOVRate")
    offsets_json["m_hZoomOwner"] = f("CCSPlayerBase_CameraServices", "m_hZoomOwner")
    offsets_json["m_flLastShotFOV"] = f("CCSPlayerBase_CameraServices", "m_flLastShotFOV")

    # Optional but useful FOV/sensitivity-related pawn values.
    offsets_json["m_flFOVSensitivityAdjust"] = f("C_BasePlayerPawn", "m_flFOVSensitivityAdjust")
    offsets_json["m_flMouseSensitivity"] = f("C_BasePlayerPawn", "m_flMouseSensitivity")

    # Weapon VData FOV/zoom characteristics.
    offsets_json["m_nZoomLevels"] = f("CCSWeaponBaseVData", "m_nZoomLevels")
    offsets_json["m_nZoomFOV1"] = f("CCSWeaponBaseVData", "m_nZoomFOV1")
    offsets_json["m_nZoomFOV2"] = f("CCSWeaponBaseVData", "m_nZoomFOV2")
    offsets_json["m_flZoomTime0"] = f("CCSWeaponBaseVData", "m_flZoomTime0")
    offsets_json["m_flZoomTime1"] = f("CCSWeaponBaseVData", "m_flZoomTime1")
    offsets_json["m_flZoomTime2"] = f("CCSWeaponBaseVData", "m_flZoomTime2")
    offsets_json["m_flIronSightFOV"] = f("CCSWeaponBaseVData", "m_flIronSightFOV")

    
    return offsets_json


def main():
    dest_path = get_path()

    if not dest_path:
        print("Invalid path for 'offsets.json'")
        raise SystemExit(1)

    try:
        build_number = get_build_number()
        if build_number == 0:
            print("Could not find the latest build number.")
            raise SystemExit(1)

        offsets = get_raw_file(urls["offsets"])
        if not offsets:
            print("Could not find the latest offsets.")
            raise SystemExit(1)

        client = get_raw_file(urls["client_dll"])
        if not client:
            print("Could not find the latest client.dll.")
            raise SystemExit(1)

        offsets_json = load_local_offsets(dest_path)

        current_build = int(offsets_json.get("build_number", 0))
        print(f"Current build number: {current_build} vs Latest build number: {build_number}")

        # Always rebuild the local JSON so new keys are added even when
        # the build number did not change.
        updated_offsets = build_updated_offsets(offsets_json, build_number, offsets, client)

        if current_build == build_number:
            print("Build number is unchanged, but refreshing all tracked offsets anyway.")
        else:
            print("Build number changed, updating local offsets.")

        save_local_offsets(dest_path, updated_offsets)
        print("Offsets updated in the local file.")

    except requests.RequestException as e:
        print(f"Network error: {e}")
        raise SystemExit(1)
    except KeyError as e:
        print(f"KeyError: {e}")
        print("The structure of the remote JSON appears to have changed. Check the source repository.")
        raise SystemExit(2)
    except json.JSONDecodeError as e:
        print(f"JSON decode error: {e}")
        raise SystemExit(1)
    except OSError as e:
        print(f"File error: {e}")
        raise SystemExit(1)


if __name__ == "__main__":
    main()
