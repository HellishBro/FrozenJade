import json
import amulet_nbt as nbt
import gzip
import base64
from websockets.client import connect

# Items

class Item:
    def __init__(self, id, data, slot=None):
        self.id = id
        self.data = data
        self.slot = slot if slot else 0

    def todict(self):
        return {
            "item": {
                "id": self.id,
                "data": self.data
            },
            "slot": self.slot
        }

class RegularItem(Item):
    def __init__(self, item_id, count, slot=None):
        super().__init__("item", {"item": nbt.CompoundTag(Count=nbt.ByteTag(count), id=nbt.StringTag(item_id)).to_snbt()}, slot=slot)

class Location(Item):
    def __init__(self, x, y, z, yaw=0, pitch=0, slot=None):
        super().__init__("loc", {"isBlock": False, "loc": {"x": x, "y": y, "z": z, "pitch": pitch, "yaw": yaw}}, slot=slot)

class Variable(Item):
    def __init__(self, varname, scope="unsaved", slot=None):
        super().__init__("var", {"name": varname, "scope": scope}, slot=slot)

class Vector(Item):
    def __init__(self, x, y, z, slot=None):
        super().__init__("vector", {"x": x, "y": y, "z": z}, slot=slot)

class BlockTag(Item):
    def __init__(self, tag, option):
        super().__init__("bl_tag", {"tag": tag, "option": option})

class Number(Item):
    def __init__(self, num, slot=None):
        super().__init__("num", {"name": str(num)}, slot=slot)

class Text(Item):
    def __init__(self, text, slot=None):
        super().__init__("txt", {"name": text}, slot=slot)

class GameValue(Item):
    def __init__(self, value, target="Default", slot=None):
        super().__init__("g_val", {"target": target, "type": value}, slot=slot)

# Objects

class Object:
    def __init__(self, category, action, arguments: list[Item] = None, **extra):
        self.category = category
        self.action = action
        self.arguments = arguments if arguments else []
        last = 0
        tags = 0
        for arg in self.arguments:
            if not arg.slot:
                if arg.id == "bl_tag":
                    arg.slot = 26 - tags
                    arg.data["action"] = action if action else "dynamic"
                    arg.data["block"] = category
                    tags += 1
                else:
                    arg.slot = last
                    last += 1
        self.extra = extra

    def todict(self):
        result = {
            "id": "block",
            "block": self.category,
            "args": {"items": [arg.todict() for arg in self.arguments]}
        }
        if self.action: result["action"] = self.action
        for i, v in self.extra.items():
            result[i] = v
        return result

class Function(Object):
    def __init__(self, name, hide):
        super().__init__("func", "", [BlockTag("Is Hidden", str(hide))], data=name)
        self.name = name

class Process(Object):
    def __init__(self, name, hide):
        super().__init__("process", "", [BlockTag("Is Hidden", str(hide))], data=name)
        self.name = name

class PlayerEvent(Object):
    def __init__(self, event):
        super().__init__("event", event, [])

class EntityEvent(Object):
    def __init__(self, event):
        super().__init__("entity_event", event, [])

class Bracket:
    def __init__(self, open=True, type="norm"):
        self.open = open
        self.type = type
    def todict(self):
        return {
            "id": "bracket",
            "type": self.type,
            "direct": "open" if self.open else "close"
        }

# Template

class Template:
    def __init__(self, blocks: list[Object]=None):
        self.blocks = blocks if blocks else []

    def add(self, *obj: Object):
        for o in obj:
            self.blocks.append(o)
        return self

    def __str__(self):
        return json.dumps(self.todict())

    def todict(self):
        return {
            "blocks": [
                b.todict() for b in self.blocks
            ]
        }

    def compress(self):
        return base64.b64encode(gzip.compress(str(self).replace("\n", "").encode())).decode()

    async def send(self, name="Imported Template", author="DFTemplates"):
        try:
            async with connect("ws://localhost:31371") as s:
                send = json.dumps({
                    "type": "template",
                    "source": author,
                    "data": json.dumps({
                        "data": self.compress(),
                        "author": author,
                        "name": name
                    })
                }) + "\n"
                await s.send(send)
        except ConnectionRefusedError:
            print("\033[31mTemplate sending cannot be done: recode is not open.")
