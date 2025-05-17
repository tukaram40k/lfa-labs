class AstNode:
    def tree_str(self, indent=0, prefix=""):
        raise NotImplementedError

class FactionDeclaration(AstNode):
    def __init__(self, faction_type, leader_name, body):
        self.faction_type = faction_type
        self.leader_name = leader_name
        self.body = body
    
    def tree_str(self, indent=0, prefix=""):
        spaces = '    ' * indent
        result = f"{spaces}{prefix}Hero: {self.faction_type}, {self.leader_name}\n"
        result += self.body.tree_str(indent + 1, "|__ ")
        return result

class DeploymentStmt(AstNode):
    def __init__(self, unit_type, count):
        self.unit_type = unit_type
        self.count = count
    
    def tree_str(self, indent=0, prefix=""):
        spaces = '    ' * indent
        return f"{spaces}{prefix}Deploy: {self.unit_type}, {self.count}\n"

class CastStmt(AstNode):
    def __init__(self, caster, ability):
        self.caster = caster
        self.ability = ability
    
    def tree_str(self, indent=0, prefix=""):
        spaces = '    ' * indent
        return f"{spaces}{prefix}Cast: {self.caster}, \"{self.ability}\"\n"

class VoxTransmissionStmt(AstNode):
    def __init__(self, sender, message):
        self.sender = sender
        self.message = message
    
    def tree_str(self, indent=0, prefix=""):
        spaces = '    ' * indent
        return f"{spaces}{prefix}Vox: {self.sender}, \"{self.message}\"\n"

class EngagementStmt(AstNode):
    def __init__(self, combatants):
        self.combatants = combatants
    
    def tree_str(self, indent=0, prefix=""):
        spaces = '    ' * indent
        result = f"{spaces}{prefix}Engagement\n"
        for i, combatant in enumerate(self.combatants):
            result += f"{spaces}    |__ Hero: \"{combatant}\"\n"
        return result

class Block(AstNode):
    def __init__(self, statements):
        self.statements = statements
    
    def tree_str(self, indent=0, prefix=""):
        spaces = '    ' * indent
        result = f"{spaces}{prefix}Army:"
        for i, stmt in enumerate(self.statements):
            result += "\n" + stmt.tree_str(indent + 1, "|__ ").rstrip()
        return result
