from bl3hotfixmod.bl3hotfixmod import Mod

mod = Mod('better_passives.wlhotfix',
        'Better Passives',
        'ZetaDaemon',
        [],
        lic=Mod.CC_BY_SA_40,
        v='1.0.0',
        )

ability_list = [
	"Ability_All_Ring_GunType_AR",
	"Ability_All_Ring_GunType_PS",
	"Ability_All_Ring_GunType_SG",
	"Ability_All_Ring_GunType_SMG",
	"Ability_All_Ring_GunType_SR",
	"SE_Ring_GunType_AR_Bonuses",
	"SE_Ring_GunType_PS_Bonuses",
	"SE_Ring_GunType_SG_Bonuses",
	"SE_Ring_GunType_SMG_Bonuses",
	"SE_Ring_GunType_SR_Bonuses"
]
for ability in ability_list:
	mod.reg_hotfix(Mod.PATCH, '',
	    f"/Game/Gear/Rings/_Shared/Design/Parts/GunTypeStats/Abilities/{ability}.Default__{ability}_C",
	    'AbilityEffects.AbilityEffects[0].Condition',
	    "()")
	mod.newline()
mod.newline()

crit_list = [
	"UIStat_PartDesc_Min_AR_CritDamage",
	"UIStat_PartDesc_Min_PS_CritDamage",
	"UIStat_PartDesc_Min_SG_CritDamage",
	"UIStat_PartDesc_Min_SR_CritDamage",
	"UIStat_PartDesc_Min_SMG_CritDamage",
]
mag_list = [
	"UIStat_PartDesc_Min_AR_MagSize",
	"UIStat_PartDesc_Min_PS_MagSize",
	"UIStat_PartDesc_Min_SR_MagSize",
	"UIStat_PartDesc_Min_SG_MagazineSize",
	"UIStat_PartDesc_Min_SMG_MagSize",
]
reload_list = [
	"UIStat_PartDesc_Min_AR_Reload",
	"UIStat_PartDesc_Min_PS_Reload",
	"UIStat_PartDesc_Min_SG_Reload",
	"UIStat_PartDesc_Min_SR_ReloadSpeed",
	"UIStat_PartDesc_Min_SMG_Reload",
]
command_list = [
	[crit_list, "[skill]$VALUE$[/skill] Gun Critical Hit Damage"],
	[mag_list, "[skill]$VALUE$[/skill] Magazine Size"],
	[reload_list, "[skill]$VALUE$[/skill] Reload Speed"]
]
for command in command_list:
	for part in command[0]:
		mod.reg_hotfix(Mod.PATCH, '',
		    f"/Game/Gear/Rings/_Shared/Design/UIStats/{part}",
		    'FormatText',
		    command[1])
		mod.newline()
	mod.newline()

mod.close()