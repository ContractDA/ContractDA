
# parsetab.py
# This file is automatically generated. Do not edit.
# pylint: disable=W,C,R
_tabversion = '3.10'

_lr_method = 'LALR'

_lr_signature = 'leftLPARENRPARENleftANDORIMPLYNOTleftGEGTLTLEEQNEQleftADDSUBleftMULDIVleftPOWERADD AND COMMENT CONSTANT DIV EQ EXIST FALSE FORALL GE GT IMPLY LAND LE LITERAL LOR LPAREN LT MUL NEQ NOT OR POWER RPAREN SUB TRUEproposition : NOT proposition\n                       | NOT expressionproposition : expression GE expression\n                   | expression GT expression\n                   | expression LT expression\n                   | expression LE expression        \n                   | expression EQ expression\n                   | expression NEQ expression    \n                   | proposition AND proposition   \n                   | proposition OR proposition   \n                   | proposition IMPLY proposition\n                   | expression EQ proposition\n                   | expression NEQ proposition\n                   | proposition EQ expression\n                   | proposition NEQ expression  proposition : LPAREN proposition RPARENproposition : TRUE\n                       | FALSE   expression : expression ADD expression\n                   | expression SUB expression\n                   | expression MUL expression\n                   | expression DIV expression\n                   | expression POWER expressionexpression : constant\n                      | symbolexpression : LPAREN expression RPARENsymbol : LITERALconstant : CONSTANT'
    
_lr_action_items = {'NOT':([0,2,4,11,12,13,22,23,43,],[2,2,2,2,2,2,2,2,2,]),'LPAREN':([0,2,4,11,12,13,14,15,18,19,20,21,22,23,24,25,26,27,28,35,43,],[4,4,4,4,4,4,35,35,35,35,35,35,43,43,35,35,35,35,35,35,43,]),'TRUE':([0,2,4,11,12,13,22,23,43,],[5,5,5,5,5,5,5,5,5,]),'FALSE':([0,2,4,11,12,13,22,23,43,],[6,6,6,6,6,6,6,6,6,]),'CONSTANT':([0,2,4,11,12,13,14,15,18,19,20,21,22,23,24,25,26,27,28,35,43,],[9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,]),'LITERAL':([0,2,4,11,12,13,14,15,18,19,20,21,22,23,24,25,26,27,28,35,43,],[10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,]),'$end':([1,5,6,7,8,9,10,16,17,31,32,33,34,36,37,38,39,40,41,42,44,45,46,47,48,49,50,51,52,],[0,-17,-18,-24,-25,-28,-27,-1,-2,-9,-10,-11,-14,-15,-3,-4,-5,-6,-7,-12,-8,-13,-19,-20,-21,-22,-23,-16,-26,]),'AND':([1,5,6,7,8,9,10,16,17,29,31,32,33,34,36,37,38,39,40,41,42,44,45,46,47,48,49,50,51,52,],[11,-17,-18,-24,-25,-28,-27,-1,-2,11,-9,-10,-11,-14,-15,-3,-4,-5,-6,-7,-12,-8,-13,-19,-20,-21,-22,-23,-16,-26,]),'OR':([1,5,6,7,8,9,10,16,17,29,31,32,33,34,36,37,38,39,40,41,42,44,45,46,47,48,49,50,51,52,],[12,-17,-18,-24,-25,-28,-27,-1,-2,12,-9,-10,-11,-14,-15,-3,-4,-5,-6,-7,-12,-8,-13,-19,-20,-21,-22,-23,-16,-26,]),'IMPLY':([1,5,6,7,8,9,10,16,17,29,31,32,33,34,36,37,38,39,40,41,42,44,45,46,47,48,49,50,51,52,],[13,-17,-18,-24,-25,-28,-27,-1,-2,13,-9,-10,-11,-14,-15,-3,-4,-5,-6,-7,-12,-8,-13,-19,-20,-21,-22,-23,-16,-26,]),'EQ':([1,3,5,6,7,8,9,10,16,17,29,30,31,32,33,34,36,37,38,39,40,41,42,44,45,46,47,48,49,50,51,52,54,],[14,22,-17,-18,-24,-25,-28,-27,14,22,14,22,14,14,14,-14,-15,-3,-4,-5,-6,-7,-12,-8,-13,-19,-20,-21,-22,-23,-16,-26,22,]),'NEQ':([1,3,5,6,7,8,9,10,16,17,29,30,31,32,33,34,36,37,38,39,40,41,42,44,45,46,47,48,49,50,51,52,54,],[15,23,-17,-18,-24,-25,-28,-27,15,23,15,23,15,15,15,-14,-15,-3,-4,-5,-6,-7,-12,-8,-13,-19,-20,-21,-22,-23,-16,-26,23,]),'GE':([3,7,8,9,10,17,30,41,44,46,47,48,49,50,52,54,],[18,-24,-25,-28,-27,18,18,18,18,-19,-20,-21,-22,-23,-26,18,]),'GT':([3,7,8,9,10,17,30,41,44,46,47,48,49,50,52,54,],[19,-24,-25,-28,-27,19,19,19,19,-19,-20,-21,-22,-23,-26,19,]),'LT':([3,7,8,9,10,17,30,41,44,46,47,48,49,50,52,54,],[20,-24,-25,-28,-27,20,20,20,20,-19,-20,-21,-22,-23,-26,20,]),'LE':([3,7,8,9,10,17,30,41,44,46,47,48,49,50,52,54,],[21,-24,-25,-28,-27,21,21,21,21,-19,-20,-21,-22,-23,-26,21,]),'ADD':([3,7,8,9,10,17,30,34,36,37,38,39,40,41,44,46,47,48,49,50,52,53,54,],[24,-24,-25,-28,-27,24,24,24,24,24,24,24,24,24,24,-19,-20,-21,-22,-23,-26,24,24,]),'SUB':([3,7,8,9,10,17,30,34,36,37,38,39,40,41,44,46,47,48,49,50,52,53,54,],[25,-24,-25,-28,-27,25,25,25,25,25,25,25,25,25,25,-19,-20,-21,-22,-23,-26,25,25,]),'MUL':([3,7,8,9,10,17,30,34,36,37,38,39,40,41,44,46,47,48,49,50,52,53,54,],[26,-24,-25,-28,-27,26,26,26,26,26,26,26,26,26,26,26,26,-21,-22,-23,-26,26,26,]),'DIV':([3,7,8,9,10,17,30,34,36,37,38,39,40,41,44,46,47,48,49,50,52,53,54,],[27,-24,-25,-28,-27,27,27,27,27,27,27,27,27,27,27,27,27,-21,-22,-23,-26,27,27,]),'POWER':([3,7,8,9,10,17,30,34,36,37,38,39,40,41,44,46,47,48,49,50,52,53,54,],[28,-24,-25,-28,-27,28,28,28,28,28,28,28,28,28,28,28,28,28,28,-23,-26,28,28,]),'RPAREN':([5,6,7,8,9,10,16,17,29,30,31,32,33,34,36,37,38,39,40,41,42,44,45,46,47,48,49,50,51,52,53,54,],[-17,-18,-24,-25,-28,-27,-1,-2,51,52,-9,-10,-11,-14,-15,-3,-4,-5,-6,-7,-12,-8,-13,-19,-20,-21,-22,-23,-16,-26,52,52,]),}

_lr_action = {}
for _k, _v in _lr_action_items.items():
   for _x,_y in zip(_v[0],_v[1]):
      if not _x in _lr_action:  _lr_action[_x] = {}
      _lr_action[_x][_k] = _y
del _lr_action_items

_lr_goto_items = {'proposition':([0,2,4,11,12,13,22,23,43,],[1,16,29,31,32,33,42,45,29,]),'expression':([0,2,4,11,12,13,14,15,18,19,20,21,22,23,24,25,26,27,28,35,43,],[3,17,30,3,3,3,34,36,37,38,39,40,41,44,46,47,48,49,50,53,54,]),'constant':([0,2,4,11,12,13,14,15,18,19,20,21,22,23,24,25,26,27,28,35,43,],[7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,]),'symbol':([0,2,4,11,12,13,14,15,18,19,20,21,22,23,24,25,26,27,28,35,43,],[8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,]),}

_lr_goto = {}
for _k, _v in _lr_goto_items.items():
   for _x, _y in zip(_v[0], _v[1]):
       if not _x in _lr_goto: _lr_goto[_x] = {}
       _lr_goto[_x][_k] = _y
del _lr_goto_items
_lr_productions = [
  ("S' -> proposition","S'",1,None,None,None),
  ('proposition -> NOT proposition','proposition',2,'p_proposition_uniop','_fol_parser.py',122),
  ('proposition -> NOT expression','proposition',2,'p_proposition_uniop','_fol_parser.py',123),
  ('proposition -> expression GE expression','proposition',3,'p_proposition_binop','_fol_parser.py',127),
  ('proposition -> expression GT expression','proposition',3,'p_proposition_binop','_fol_parser.py',128),
  ('proposition -> expression LT expression','proposition',3,'p_proposition_binop','_fol_parser.py',129),
  ('proposition -> expression LE expression','proposition',3,'p_proposition_binop','_fol_parser.py',130),
  ('proposition -> expression EQ expression','proposition',3,'p_proposition_binop','_fol_parser.py',131),
  ('proposition -> expression NEQ expression','proposition',3,'p_proposition_binop','_fol_parser.py',132),
  ('proposition -> proposition AND proposition','proposition',3,'p_proposition_binop','_fol_parser.py',133),
  ('proposition -> proposition OR proposition','proposition',3,'p_proposition_binop','_fol_parser.py',134),
  ('proposition -> proposition IMPLY proposition','proposition',3,'p_proposition_binop','_fol_parser.py',135),
  ('proposition -> expression EQ proposition','proposition',3,'p_proposition_binop','_fol_parser.py',136),
  ('proposition -> expression NEQ proposition','proposition',3,'p_proposition_binop','_fol_parser.py',137),
  ('proposition -> proposition EQ expression','proposition',3,'p_proposition_binop','_fol_parser.py',138),
  ('proposition -> proposition NEQ expression','proposition',3,'p_proposition_binop','_fol_parser.py',139),
  ('proposition -> LPAREN proposition RPAREN','proposition',3,'p_proposition_paren','_fol_parser.py',142),
  ('proposition -> TRUE','proposition',1,'p_proposition_literal','_fol_parser.py',146),
  ('proposition -> FALSE','proposition',1,'p_proposition_literal','_fol_parser.py',147),
  ('expression -> expression ADD expression','expression',3,'p_expression_binop','_fol_parser.py',151),
  ('expression -> expression SUB expression','expression',3,'p_expression_binop','_fol_parser.py',152),
  ('expression -> expression MUL expression','expression',3,'p_expression_binop','_fol_parser.py',153),
  ('expression -> expression DIV expression','expression',3,'p_expression_binop','_fol_parser.py',154),
  ('expression -> expression POWER expression','expression',3,'p_expression_binop','_fol_parser.py',155),
  ('expression -> constant','expression',1,'p_expression_literal','_fol_parser.py',160),
  ('expression -> symbol','expression',1,'p_expression_literal','_fol_parser.py',161),
  ('expression -> LPAREN expression RPAREN','expression',3,'p_expression_paren','_fol_parser.py',165),
  ('symbol -> LITERAL','symbol',1,'p_symbol','_fol_parser.py',169),
  ('constant -> CONSTANT','constant',1,'p_constant','_fol_parser.py',179),
]
