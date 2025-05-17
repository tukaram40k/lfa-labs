from lexer import TokenType
from tree import *

class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.current_token = None
        self.pos = -1
        self.advance()
    
    def advance(self):
        self.pos += 1
        if self.pos < len(self.tokens):
            self.current_token = self.tokens[self.pos]
        return self.current_token
    
    def expect(self, token_type, err_msg):
        if not self.current_token or self.current_token.type != token_type:
            raise SyntaxError(f"HERESY! {err_msg} at position {self.current_token.pos if self.current_token else 'EOF'}")
        value = self.current_token.value
        self.advance()
        return value
    
    def parse(self):
        ast = []
        while self.current_token and self.current_token.type != TokenType.eof:
            if self.current_token.type == TokenType.faction:
                ast.append(self.parse_faction())
            elif self.current_token.type == TokenType.engage:
                ast.append(self.parse_engagement())
            else:
                raise SyntaxError(f"UNEXPECTED COMMAND: {self.current_token.value} (type: {self.current_token.type.value})")
        return ast
    
    def parse_faction(self):
        faction_type = self.expect(TokenType.faction, "Expected faction declaration")
        leader_name = self.expect(TokenType.str, "Expected leader name in high gothic")
        self.expect(TokenType.lpar, "Expected '{' to begin faction block")

        statements = []
        while self.current_token and self.current_token.type != TokenType.rpar:
            if self.current_token.type == TokenType.deploy:
                statements.append(self.parse_deployment())
            elif self.current_token.type == TokenType.identifier:
                unit_name = self.current_token.value
                self.advance()
                if self.current_token.type == TokenType.cast:
                    statements.append(self.parse_cast(unit_name))
                elif self.current_token.type == TokenType.vox:
                    statements.append(self.parse_vox_transmission(unit_name))
                else:
                    raise SyntaxError(f"UNKNOWN ACTION FOR UNIT {unit_name}")
            else:
                raise SyntaxError(f"UNKNOWN COMMAND IN FACTION BLOCK: {self.current_token.value} (type: {self.current_token.type.value})")

        self.expect(TokenType.rpar, "Expected '}' to end faction block")
        return FactionDeclaration(faction_type, leader_name, Block(statements))
    
    def parse_deployment(self):
        self.expect(TokenType.deploy, "Expected 'deploy' command")
        unit_type = self.expect(TokenType.identifier, "Expected unit type")
        self.expect(TokenType.equals, "Expected '=' in deployment")
        count = self.expect(TokenType.num, "Expected unit count")
        return DeploymentStmt(unit_type, count)
    
    def parse_cast(self, unit_name=None):
        if unit_name is None:
            unit_name = self.expect(TokenType.identifier, "Expected caster identifier")
        self.expect(TokenType.cast, "Expected 'cast' command")
        ability = self.expect(TokenType.str, "Expected ability name in high gothic")
        return CastStmt(unit_name, ability)

    def parse_vox_transmission(self, unit_name=None):
        if unit_name is None:
            unit_name = self.expect(TokenType.identifier, "Expected sender identifier")
        self.expect(TokenType.vox, "Expected 'vox_transmit' command")
        message = self.expect(TokenType.str, "Expected vox message in high gothic")
        return VoxTransmissionStmt(unit_name, message)
    
    def parse_engagement(self):
        self.expect(TokenType.engage, "Expected 'engage' command")
        self.expect(TokenType.lpar, "Expected '{' to begin engagement block")
        
        combatants = []
        while self.current_token and self.current_token.type != TokenType.rpar:
            combatant = self.expect(TokenType.str, "Expected combatant name in high gothic")
            combatants.append(combatant)
        
        self.expect(TokenType.rpar, "Expected '}' to end engagement block")
        return EngagementStmt(combatants)
    
    def print_tree(self, tree):
        print("\nBattle Start")
        for i, node in enumerate(tree):
            print(node.tree_str(1, "|__ "))
