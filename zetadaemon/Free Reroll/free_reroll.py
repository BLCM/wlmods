from bl3hotfixmod.bl3hotfixmod import Mod, BVC, BVCF

mod = Mod('free_reroll.wlhotfix',
        'Free Reroll',
        'ZetaDaemon',
        [],
        lic=Mod.CC_BY_SA_40,
        v='1.0.0',
        )


mod.table_hotfix(Mod.PATCH, '',
    '/Game/GameData/Economy/Economy_MoonOrbs',
    'ReRollCostCap',
    'Value',
     BVC(bvs=0))
mod.newline()
mod.table_hotfix(Mod.PATCH, '',
    '/Game/GameData/Economy/Economy_MoonOrbs',
    'BaseCost',
    'Value',
    BVC(bvs=0))

mod.close()