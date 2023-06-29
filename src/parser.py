from lark import Lark, Token, Transformer, Discard

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

truc_parser = Lark(r"""
                    file: (w instruction? w "\n")*

                    instruction: "." WORD -> label
                           | "store" wp mem_address wp register -> store
                           | binop wp register wp register wp register -> binop
                           | "mov" wp register wp register -> mov
                           | "mov" wp register wp register -> mov
                           | jump wp WORD -> jump

                    binop: "add" -> add
                        | "sub"  -> sub
                        | "or"   -> or
                        | "xor"  -> xor

                    jump: "jmp"  -> jmp
                        | "jz"   -> jz
                        | "jneg" -> jneg
                        | "jof"  -> jof

                    register: "%" NUMBER
                    mem_address: "#" NUMBER
                    immediate: "$" NUMBER

                    w: WS*
                    wp: WS+
                    %import common.WORD
                    %import common.NUMBER
                    %import common.WS

                    COMMENT: "--" /[^\n]/* 
                    %ignore COMMENT

                   """, start = "file")

text = r"""
.abcsd
    -- thing
    store #12 %5 --test
    add %0 %2 %3
    or %0 %0 %0
    sub %0 %0 %0

.issou
    mov %2 %5
    jz issou -- Jump

"""

class SpaceTransformer(Transformer):
    def w(self, tok: Token):
        return Discard
    def wp(self, tok: Token):
        return Discard

parsed = SpaceTransformer().transform(truc_parser.parse(text))
print(parsed)
print(parsed.pretty())
