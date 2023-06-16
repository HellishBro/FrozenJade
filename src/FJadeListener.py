# Generated from FJade.g4 by ANTLR 4.12.0
import random
import string

from antlr4 import *
if __name__ is not None and "." in __name__:
    from .FJadeParser import FJadeParser
    from . import DFTemplates as dft
else:
    from FJadeParser import FJadeParser
    import DFTemplates as dft

def string(ctx, i=0):
    try:
        return ctx.STRING(i).getText()[1:-1].replace("&", "§")
    except TypeError:
        return ctx.STRING().getText()[1:-1].replace("&", "§")

def number(ctx, i=0, method=float):
    try:
        return method(ctx.NUMBER(i).getText()) if ctx.NUMBER(i) else 0
    except TypeError:
        return method(ctx.NUMBER().getText())

def create_array(items, varobj):
    final = []
    current_args = [varobj]
    for i in items:
        if len(current_args) == 26:
            final.append(dft.Object(
                "set_var", "AppendList" if final else "CreateList", current_args
            ))
            current_args = [varobj]
        current_args.append(i)
    if len(current_args) > 1:
        final.append(dft.Object(
            "set_var", "AppendList" if final else "CreateList", current_args
        ))
    return final

def random_string():
    return "".join([random.choice(string.ascii_letters) for _ in range(random.randint(5, 11))])

var_scopes = {
    "s": "saved",
    "saved": "saved",
    "l": "local",
    "local": "local",
    "g": "unsaved",
    "unsaved": "unsaved",
    "global": "unsaved",
}

# This class defines a complete listener for a parse tree produced by FJadeParser.
class FJadeListener(ParseTreeListener):

    # Initialization of parser.
    def __init__(self):
        self.template = dft.Template()

    # Enter a parse tree produced by FJadeParser#fjade.
    def enterFjade(self, ctx:FJadeParser.FjadeContext):
        pass

    # Exit a parse tree produced by FJadeParser#fjade.
    def exitFjade(self, ctx:FJadeParser.FjadeContext):
        pass


    # Enter a parse tree produced by FJadeParser#func.
    def enterFunc(self, ctx: FJadeParser.FuncContext):
        self.template.add(
            dft.Function(ctx.NAME().getText(), False)
        )

    # Exit a parse tree produced by FJadeParser#func.
    def exitFunc(self, ctx:FJadeParser.FuncContext):
        pass


    # Enter a parse tree produced by FJadeParser#proc.
    def enterProc(self, ctx: FJadeParser.ProcContext):
        self.template.add(
            dft.Process(ctx.NAME().getText(), False)
        )

    # Exit a parse tree produced by FJadeParser#proc.
    def exitProc(self, ctx:FJadeParser.ProcContext):
        pass


    # Enter a parse tree produced by FJadeParser#playerev.
    def enterPlayerev(self, ctx: FJadeParser.PlayerevContext):
        self.template.add(
            dft.PlayerEvent(ctx.NAME().getText())
        )

    # Exit a parse tree produced by FJadeParser#playerev.
    def exitPlayerev(self, ctx:FJadeParser.PlayerevContext):
        pass


    # Enter a parse tree produced by FJadeParser#entityev.
    def enterEntityev(self, ctx:FJadeParser.EntityevContext):
        self.template.add(
            dft.EntityEvent(ctx.NAME().getText())
        )

    # Exit a parse tree produced by FJadeParser#entityev.
    def exitEntityev(self, ctx:FJadeParser.EntityevContext):
        pass


    # Enter a parse tree produced by FJadeParser#stmt.
    def enterStmt(self, ctx:FJadeParser.StmtContext):
        pass

    # Exit a parse tree produced by FJadeParser#stmt.
    def exitStmt(self, ctx:FJadeParser.StmtContext):
        pass


    # Enter a parse tree produced by FJadeParser#simplestmt.
    def enterSimplestmt(self, ctx: FJadeParser.SimplestmtContext):
        args = []
        for expr in ctx.paramslist().expr():
            args.append(self.enterExpr(expr))
        invert = {"inverted": "NOT"} if ctx.NEGATE() else {}
        target = {"target": ctx.TARGET().getText()} if ctx.TARGET() else {}
        tags = []
        i = 0
        while ctx.STRING(i):
            tags.append(dft.BlockTag(
                string(ctx, i),
                string(ctx, i + 1)
            ))
            i += 2
        args.extend(tags)
        kwargs = invert.copy()
        kwargs.update(target)
        if "CALL" in ctx.CATEGORY().getText():
            kwargs["data"] = ctx.NAME().getText()
        self.template.add(
            dft.Object(ctx.CATEGORY().getText().lower(), ctx.NAME().getText(), args, **kwargs)
        )

    # Exit a parse tree produced by FJadeParser#simplestmt.
    def exitSimplestmt(self, ctx:FJadeParser.SimplestmtContext):
        pass


    # Enter a parse tree produced by FJadeParser#blockedstmt.
    def enterBlockedstmt(self, ctx:FJadeParser.BlockedstmtContext):
        pass

    # Exit a parse tree produced by FJadeParser#blockedstmt.
    def exitBlockedstmt(self, ctx:FJadeParser.BlockedstmtContext):
        pass


    # Enter a parse tree produced by FJadeParser#elsestmt.
    def enterElsestmt(self, ctx: FJadeParser.ElsestmtContext):
        self.template.add([
            dft.Object("else", ""),
            dft.Bracket()]
        )

    # Exit a parse tree produced by FJadeParser#elsestmt.
    def exitElsestmt(self, ctx: FJadeParser.ElsestmtContext):
        self.template.add(
            dft.Bracket(False)
        )


    # Enter a parse tree produced by FJadeParser#classicblockedstmt.
    def enterClassicblockedstmt(self, ctx:FJadeParser.ClassicblockedstmtContext):
        self.enterSimplestmt(ctx)
        t = "norm"
        if ctx.CATEGORY().getText().lower() == "repeat":
            t = "repeat"
        self.template.add(
            dft.Bracket(True, t)
        )

    # Exit a parse tree produced by FJadeParser#classicblockedstmt.
    def exitClassicblockedstmt(self, ctx: FJadeParser.ClassicblockedstmtContext):
        t = "norm"
        if ctx.CATEGORY().getText().lower() == "repeat":
            t = "repeat"
        self.template.add(
            dft.Bracket(False, t)
        )


    # Enter a parse tree produced by FJadeParser#paramslist.
    def enterParamslist(self, ctx:FJadeParser.ParamslistContext):
        pass

    # Exit a parse tree produced by FJadeParser#paramslist.
    def exitParamslist(self, ctx:FJadeParser.ParamslistContext):
        pass


    # Enter a parse tree produced by FJadeParser#expr.
    def enterExpr(self, ctx: FJadeParser.ExprContext):
        if ctx.NAME():
            return dft.Variable(ctx.NAME().getText())
        elif ctx.NUMBER():
            return dft.Number(number(ctx))
        elif ctx.STRING():
            return dft.Text(string(ctx))
        elif ctx.item():
            return self.enterItem(ctx.item())
        elif ctx.vector():
            return self.enterVector(ctx.vector())
        elif ctx.location():
            return self.enterLocation(ctx.location())
        elif ctx.variable():
            try:
                return self.enterStringVar(ctx.variable())
            except:
                try:
                    return self.enterNameVar(ctx.variable())
                except:
                    return self.enterSimpleVar(ctx.variable())
        elif ctx.gval():
            return self.enterGval(ctx.gval())
        elif ctx.array():
            return self.enterArray(ctx.array())
        elif ctx.dictionary():
            return self.enterDictionary(ctx.dictionary())
        elif ctx.potion():
            return self.enterPotion(ctx.potion())
        elif ctx.sound():
            return self.enterSound(ctx.sound())
        elif ctx.particle():
            return self.enterParticle(ctx.particle())
        else:
            return dft.Number(0)

    # Exit a parse tree produced by FJadeParser#expr.
    def exitExpr(self, ctx:FJadeParser.ExprContext):
        pass


    # Enter a parse tree produced by FJadeParser#vector.
    def enterVector(self, ctx: FJadeParser.VectorContext):
        return dft.Vector(
            number(ctx),
            number(ctx, 1),
            number(ctx, 2)
        )

    # Exit a parse tree produced by FJadeParser#vector.
    def exitVector(self, ctx:FJadeParser.VectorContext):
        pass


    # Enter a parse tree produced by FJadeParser#location.
    def enterLocation(self, ctx: FJadeParser.LocationContext):
        return dft.Location(
            number(ctx),
            number(ctx, 1),
            number(ctx, 2),
            number(ctx, 3),
            number(ctx, 4)
        )

    # Exit a parse tree produced by FJadeParser#location.
    def exitLocation(self, ctx:FJadeParser.LocationContext):
        pass


    # Enter a parse tree produced by FJadeParser#item.
    def enterItem(self, ctx: FJadeParser.ItemContext):
        return dft.RegularItem(string(ctx), number(ctx, method=int))

    # Exit a parse tree produced by FJadeParser#item.
    def exitItem(self, ctx:FJadeParser.ItemContext):
        pass


    # Enter a parse tree produced by FJadeParser#SimpleVar.
    def enterSimpleVar(self, ctx:FJadeParser.SimpleVarContext):
        return dft.Variable(ctx.NAME().getText())

    # Exit a parse tree produced by FJadeParser#SimpleVar.
    def exitSimpleVar(self, ctx:FJadeParser.SimpleVarContext):
        pass


    # Enter a parse tree produced by FJadeParser#NameVar.
    def enterNameVar(self, ctx:FJadeParser.NameVarContext):
        if ctx.STRING():
            return dft.Variable(
                ctx.NAME().getText(), var_scopes.get(string(ctx), "unsaved")
            )
        else:
            return dft.Variable(
                ctx.NAME().getText()
            )

    # Exit a parse tree produced by FJadeParser#NameVar.
    def exitNameVar(self, ctx:FJadeParser.NameVarContext):
        pass


    # Enter a parse tree produced by FJadeParser#StringVar.
    def enterStringVar(self, ctx:FJadeParser.StringVarContext):
        if ctx.STRING(1):
            return dft.Variable(
                string(ctx, 0), var_scopes.get(string(ctx, 1), "unsaved")
            )
        else:
            return dft.Variable(
                string(ctx, 0)
            )

    # Exit a parse tree produced by FJadeParser#StringVar.
    def exitStringVar(self, ctx:FJadeParser.StringVarContext):
        pass


    # Enter a parse tree produced by FJadeParser#gval.
    def enterGval(self, ctx:FJadeParser.GvalContext):
        return dft.GameValue(
            string(ctx),
            ctx.TARGET().getText()
        )

    # Exit a parse tree produced by FJadeParser#gval.
    def exitGval(self, ctx:FJadeParser.GvalContext):
        pass


    # Enter a parse tree produced by FJadeParser#array.
    def enterArray(self, ctx:FJadeParser.ArrayContext):
        turned_list = []
        i = 0
        while ctx.expr(i):
            turned_list.append(self.enterExpr(ctx.expr(i)))
            i += 1
        temp_var = dft.Variable(random_string(), "local")
        created = create_array(turned_list, temp_var)
        self.template.add(created)
        return temp_var

    # Exit a parse tree produced by FJadeParser#array.
    def exitArray(self, ctx:FJadeParser.ArrayContext):
        pass


    # Enter a parse tree produced by FJadeParser#dictionary.
    def enterDictionary(self, ctx:FJadeParser.DictionaryContext):
        keys = []
        values = []
        i = 0
        while ctx.STRING(i):
            keys.append(string(ctx, i))
            values.append(self.enterExpr(ctx.expr(i)))
        key_var = create_array(keys, dft.Variable("k", "local", 0))
        val_var = create_array(values, dft.Variable("v", "local", 0))
        temp_var = dft.Variable(random_string(), "local")
        self.template.add(dft.Object(
            "set_var", "CreateDict", [temp_var, key_var, val_var]
        ))
        return temp_var

    # Exit a parse tree produced by FJadeParser#dictionary.
    def exitDictionary(self, ctx:FJadeParser.DictionaryContext):
        pass


    # Enter a parse tree produced by FJadeParser#potion.
    def enterPotion(self, ctx:FJadeParser.PotionContext):
        return dft.Potion(
            string(ctx), number(ctx), number(ctx, 1)
        )

    # Exit a parse tree produced by FJadeParser#potion.
    def exitPotion(self, ctx:FJadeParser.PotionContext):
        pass


    # Enter a parse tree produced by FJadeParser#sound.
    def enterSound(self, ctx:FJadeParser.SoundContext):
        return dft.Sound(
            string(ctx), number(ctx), number(ctx, 1)
        )

    # Exit a parse tree produced by FJadeParser#sound.
    def exitSound(self, ctx:FJadeParser.SoundContext):
        pass


    # Enter a parse tree produced by FJadeParser#particle.
    def enterParticle(self, ctx:FJadeParser.ParticleContext):
        material = self.enterPartMaterial(ctx.partMaterial())
        cluster = self.enterPartCluster(ctx.partCluster)
        return dft.Particle(
            material[0], cluster[0], (cluster[1], cluster[2]), material[1], material[2], material[3]
        )

    # Exit a parse tree produced by FJadeParser#particle.
    def exitParticle(self, ctx:FJadeParser.ParticleContext):
        pass


    # Enter a parse tree produced by FJadeParser#partMaterial.
    def enterPartMaterial(self, ctx:FJadeParser.PartMaterialContext):
        return string(ctx), ctx.HEX().getText()[1:], number(ctx)

    # Exit a parse tree produced by FJadeParser#partMaterial.
    def exitPartMaterial(self, ctx:FJadeParser.PartMaterialContext):
        pass


    # Enter a parse tree produced by FJadeParser#partCluster.
    def enterPartCluster(self, ctx:FJadeParser.PartClusterContext):
        return number(ctx), number(ctx, 1), number(ctx, 2)

    # Exit a parse tree produced by FJadeParser#partCluster.
    def exitPartCluster(self, ctx:FJadeParser.PartClusterContext):
        pass



del FJadeParser