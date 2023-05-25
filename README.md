
# FrozenJade

FrozenJade is an intermediate language designed to be transpiled into DiamondFire Templates with relative ease.
## Installation

This project doesn't currently have a stable release. Install `python3` or `python` from [python.org](https://python.org)

After this, ensure python is installed correctly and added to path by typing this into the command line: `py`. You should see the following messages pop up:

```sh
Python 3.10.2 (tags/v3.10.2:a58ebcc, Jan 17 2022, 14:12:15) [MSC v.1929 64 bit (AMD64)] on win32
Type "help", "copyright", "credits" or "license" for more information.
>>> 
```

type `exit()` and then:

```bash
pip install antlr4-python3-runtime
pip install amulet-nbt
```

then, `cd` into `FrozenJade` directory (one with the init file and the src directory) and you can start working from there.
    
## Usage

Command-Line syntax:
```bash
py __init__.py transpile "input/file.fjade" --stdout --compress --send
```

## Examples

#### Randomize Block Drops
```fjade
EVENT BreakBlock {
    GAME_ACTION CancelEvent;
    SET_VAR = drops [
        "dirt"
        "grass_block"
        "grass"
        "cobblestone"
        "coal"
        "granite"
        "gravel"
        "bread"
        "apple"
        "oak_plank"
        "coal"
        "iron_ingot"
        "gold_ingot"
        "sand"
    ];
    SET_VAR ListLength var("len", "l") drops;
    SET_VAR RandomNumber var("rnd", "l") 1 var("len", "l");
    SET_VAR GetListValue var("chosen one", "l") drops var("rnd", "l");
    GAME_ACTION SetBlock "air" val("Event Block Location", Default);
    SET_VAR SetItemType var("chosen one", "l") item("stone", 1) var("chosen one", "l");
    GAME_ACTION SpawnItem var("chosen one", "l") val("Event Block Location", Default);
}
```

#### Join Message
```fjade
EVENT Join {
    IF_VAR VarExists var("%default existed", "saved") ! {
        SET_VAR = var("%default existed", "saved") 1;
        SET_VAR += var("unique joins", "saved");
        PLAYER_ACTION SendMessage "&e%default just joined for the first time! &8#%var(unique joins)" @AllPlayers;
        PLAYER_ACTION PlaySound snd("Pling", 1, 2) @AllPlayers;
    } ELSE {
        PLAYER_ACTION SendMessage "&a%default joined!" @AllPlayers;
        PLAYER_ACTION PlaySound snd("Experience Orb Pickup", 1, 2) @AllPlayers;
    }
}
```

#### Parkour
```fjade
EVENT Sneak {
    IF_PLAYER StandingOn item("netherite_block", 1) { // Or you can use the string representation of the item here
        SET_VAR = var("%default timestamp", "g") val("Timestamp", Default);
        SET_VAR = var("%default checkpoint", "g") val("Location", Default);
        PLAYER_ACTION ActionBar "&eStarted!";
        PLAYER_ACTION PlaySound snd("Pling", 1, 2);
        PLAYER_ACTION SetAllowFlight |"Allow Flight": "Disable";
    }
    IF_PLAYER StandingOn item("gold_block", 1) {
        IF_VAR = var("%default timestamp", "g") 0 ! {
            SET_VAR = var("%default checkpoint", "g") val("Location", Default);
            PLAYER_ACTION PlaySound snd("Experience Orb Pickup", 1, 2);
        }
    }
    IF_PLAYER StandingOn item("diamond_block", 1) {
        IF_VAR = var("%default timestamp", "g") 0 ! {
            SET_VAR - var(t, "l") val("Timestamp", Default) var("%default timestamp", "g");
            SET_VAR RoundNumber var(t, "l");
            PLAYER_ACTION SendMessage "&e%default finished the parkour in %var(t) seconds!" @AllPlayers;
            PLAYER_ACTION SetAllowFlight |"Allow Flight": "Enable";
            SET_VAR = var("%default timestamp", "g") 0;
        }
    }
}
```
## Acknowledgements

 - [Antlr4 Project](https://www.antlr.org/)
 - [Amulet NBT](https://github.com/Amulet-Team/Amulet-NBT)

