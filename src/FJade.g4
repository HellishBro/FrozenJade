grammar FJade;

MULTILINECOMMENT: '/*' .*? '*/' -> skip;
NL: [\n\r]+ -> skip;
COMMENT: '//' .*? ('\n' | EOF) -> skip;
WS: [ \t\f]+ -> skip;

fjade: func EOF
| proc EOF
| playerev EOF
| entityev EOF;

func: 'FUNCTION' NAME '{' stmt* '}';

proc: 'PROCESS' NAME '{' stmt* '}';

playerev: ('PLAYER_EVENT' | 'EVENT') NAME '{' stmt* '}';
entityev: 'ENTITY_EVENT' NAME '{' stmt* '}';

stmt: simplestmt
| blockedstmt;

simplestmt: CATEGORY NAME paramslist ('|' STRING ':' STRING)* ('!')? ('@' TARGET)? ';';
blockedstmt: classicblockedstmt
| elsestmt;

elsestmt: 'ELSE' '{' stmt* '}';
classicblockedstmt: CATEGORY NAME paramslist ('|' STRING ':' STRING)* ('!')? ('@' TARGET)? '{' stmt* '}';

paramslist: expr*;
expr: STRING
| NUMBER
| NAME
| vector
| location
| item
| variable
| gval
| array // controversial
| dictionary // controversial
| potion
| sound
| particle;

vector: '<' NUMBER ',' NUMBER ',' NUMBER '>';
location: 'loc' '(' NUMBER ',' NUMBER ',' NUMBER (',' NUMBER ',' NUMBER)? ')';
item: 'item' '(' STRING ',' NUMBER ')';
variable: NAME # SimpleVar
| 'var' '(' NAME ',' STRING ')' # NameVar
| 'var' '(' STRING ',' STRING ')' # StringVar;
gval: 'val' '(' STRING ',' TARGET ')';
array: '[' expr* ']';
dictionary: '{' (STRING ':' expr)* '}';

potion: 'pot' '(' STRING ',' NUMBER ',' NUMBER ')';
sound: 'snd' '(' STRING ',' NUMBER ',' NUMBER ')';
particle: 'part' '(' partMaterial (',' partCluster)? ')';
partMaterial: STRING HEX ('(' NUMBER ')')?;
partCluster: NUMBER '{' NUMBER ',' NUMBER '}';

HEX: '#' ('0'..'9' | 'A'..'F')('0'..'9' | 'A'..'F')('0'..'9' | 'A'..'F')('0'..'9' | 'A'..'F')('0'..'9' | 'A'..'F')('0'..'9' | 'A'..'F');
TARGET: 'AllPlayers' | 'Selection' | 'Default' | 'Victim' | 'Killer' | 'Damager' | 'Shooter' | 'Projectile' | 'LastEntity';

ELSE: 'ELSE';
FUNCTION: 'FUNCTION';
PROCESS: 'PROCESS';
PLAYEREVENT: 'PLAYER_EVENT';
PLAYEREVENTALT: 'EVENT';
ENTITYEVENT: 'ENTITY_EVENT';

LOCATION: 'loc';
ITEM: 'item';
VARIABLE: 'var';
VALUE: 'val';
POTION: 'pot';
SOUND: 'snd';
PARTICLE: 'part';

CBRACE: '{}';
LBRACE: '{';
RBRACE: '}';
LESSTHAN: '<';
GREATERTHAN: '>';
LBRACK: '[';
RBRACK: ']';
SEMI: ';';
COLON: ':';
COMMA: ',';
NEGATE: '!';
SELECTOR: '@';
PIPE: '|';

STRING: '"' .*? '"';

NUMBER: ('0'..'9')+('.'('0'..'9') +)?;
CATEGORY: ('A'..'Z' | '_')+;
NAME: PName (PName | '0'..'9')*;
fragment PName: ('a'..'z' | 'A'..'Z' | '<' | '>' | '=' | '!' | '+' | '-' | '/' | '%');