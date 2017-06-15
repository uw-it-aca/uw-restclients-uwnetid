from commonconf import override_settings

FUWNETID = 'restclients.dao_implementation.uwnetid.File'
fdao_uwnetid_override = override_settings(
    RESTCLIENTS_UWNETID_DAO_CLASS=FUWNETID)
