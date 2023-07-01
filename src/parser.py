from lark import Lark, Token, Transformer, Discard, Tree

"""
file:
    | instructions = list(instruction) EOF {instructions}
;

instruction:
    | l = LABEL {LABEL(l)}
    | STORE r = REGISTER m = MEMADRESS {STORE(r, m)}
    | LOAD r = REGISTER m = MEMADRESS {LOAD(r, m)}
    | ADD r1 = REGISTER r2 = REGISTER r3 = REGISTER {ADD(r1, r2, r3)}
    | SUB r1 = REGISTER r2 = REGISTER r3 = REGISTER {SUB(r1, r2, r3)}
    | XOR r1 = REGISTER r2 = REGISTER r3 = REGISTER {XOR(r1, r2, r3)}
    | OR r1 = REGISTER r2 = REGISTER r3 = REGISTER {OR(r1, r2, r3)}
    | LOADI i = IMMEDIATE r = REGISTER {LOADI(i, r)}
    | JMP r = LABEL_OCC {JMP r}
    | JZ r = LABEL_OCC {JZ r}
    | JNEG r = LABEL_OCC {JNEG r}
    | JOF r = LABEL_OCC {JOF r}
    | NOP {ADD(0, 0, 0)}
    | MOV r1 = REGISTER r2 = REGISTER {ADD(r1, 0, r2)}
    | PRINT r = REGISTER i = IMMEDIATE {PRINT(r, i)}
;
"""

truc_parser = Lark(
    r"""
                    ?file: (w instruction? w "\n")*(w instruction? w)?

                    ?instruction: "." WORD -> label
                           | "store" wp mem_address wp register -> store
                           | binop wp register wp register wp register -> binop
                           | "mov" wp register wp register -> mov
                           | "mov" wp register wp register -> mov
                           | jump wp WORD -> jump
                           | "loadi" wp immediate wp register -> loadi
                           | "nop" -> nop

                    binop: "add" -> add
                        | "sub"  -> sub
                        | "or"   -> or
                        | "xor"  -> xor

                    jump: "jmp"  -> jmp
                        | "jz"   -> jz
                        | "jneg" -> jneg
                        | "jof"  -> jof

                    register: "%" NUMBER
                    mem_address: "@" NUMBER
                    immediate: "$" NUMBER

                    w: WS*
                    wp: WS+
                    %import common.WORD
                    %import common.NUMBER
                    %import common.WS

                    COMMENT: "#" /[^\n]/* 
                    %ignore COMMENT

                   """,
    start="file",
)

text = r""".abcsd
    # thing
    store @12 %5 #test
    add %0 %2 %30
    jmp abcsd
    or %0 %15 %1
    loadi $1 %17
    sub %0 %0 %5
    nop

.issou
    mov %2 %5
    jz issou # Jump
"""


class SpaceTransformer(Transformer):
    def w(self, tok: Token):
        return Discard

    def wp(self, tok: Token):
        return Discard

    def loadi(self, tok: Token):
        reg_id = int(tok[-1].children[0].value)
        if reg_id in [0, 1, 15]:
            print(
                f"Register is not writable: {tok[-1].children[0].value}, line {tok[-1].children[0].line}"
            )
        if (reg_id > 15) or (reg_id < 0):
            print(
                f"Register id out-of-range: {reg_id}, line {tok[-1].children[0].line}"
            )
        return Tree(tok[0].data, children=tok[1:])

    def binop(self, tok: Token):
        for reg in tok[1:]:
            reg_id = int(reg.children[0].value)
            if (reg_id > 15) or (reg_id < 0):
                print(
                    f"Register id out-of-range: {reg_id}, line {reg.children[0].line}"
                )
        if int(tok[-1].children[0].value) in [0, 1, 15]:
            print(
                f"Register is not writable: {tok[-1].children[0].value}, line {tok[-1].children[0].line}"
            )
        return Tree(tok[0].data, children=tok[1:])


# Performs the label extraction and removal
class LabelRecorder:
    labels = {}
    instructions = []
    pc = 0

    def file(self, tree):
        for tree in tree.children:
            if self.instruction(tree):
                self.pc += 1
                self.instructions.append(tree)
        return (self.instructions, self.labels)

    def instruction(self, tree):
        if tree.data == "label":
            self.label(tree)
            return False
        return True

    def label(self, tree):
        new_label = tree.children[0]
        new_location = self.pc
        # print(f"{new_location}: {new_label}")
        self.labels[new_label] = new_location


parsed = truc_parser.parse(text)
parsed_nospaces = SpaceTransformer().transform(parsed)
# print(parsed_nospaces)
# print(parsed_nospaces.pretty())
tree, labels = LabelRecorder().file(parsed_nospaces)
print(labels)
print(Tree(data="file", children=tree).pretty())
