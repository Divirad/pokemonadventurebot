
def create_tables(cursor):

    cursor.execute("""
        CREATE TABLE type (
        id int NOT NULL PRIMARY KEY,
        name varchar(10) NOT NULL,
        is_physical bool NOT NULL
        );

        CREATE TABLE type_efficiencies (
        attack int NOT NULL,
        defense int NOT NULL,
        effective int NOT NULL,

        Primary key (attack, defense),
        UNIQUE INDEX (attack, defense),
        Foreign Key (defense) References type(id),
        Foreign Key (attack) References type(id)
        );

        CREATE TABLE growth_rate (
            id int NOT NULL PRIMARY KEY,
            name varchar(12) NOT NULL
        );
    
        CREATE TABLE pokespecies (
        id int NOT NULL PRIMARY KEY,
        type1 int NOT NULL,
        type2 int,
        name varchar(18) CHARACTER SET utf8 NOT NULL,
        catchrate int NOT NULL,
        pokedextext text NOT NULL,
        hp_base int NOT NULL,
        attack_base int NOT NULL,
        defense_base int NOT NULL,
        special_base int NOT NULL,
        speed_base int NOT NULL,
        exp_base int NOT NULL,
        growth_rate int NOT NULL,
        gender char(1) DEFAULT NULL,

        Foreign Key (growth_rate) References growth_rate(id),
        Foreign Key (type1) References type(id),
        Foreign Key (type2) References type(id)
        );

        CREATE TABLE move_effect (
        id int NOT NULL PRIMARY KEY,
        name text NOT NULL
        );

        CREATE TABLE move (
        id int NOT NULL PRIMARY KEY,
        name text NOT NULL,
        type int NOT NULL,
        priority int NOT NULL,
        power int,
        accuracy int,
        pp int,
        effect int,

        Foreign Key (type) References type(id),
        Foreign Key (effect) References move_effect(id)
        );

        CREATE TABLE learnable_moves (
        species_id int NOT NULL,
        move_id int NOT NULL,
        learning_by int NOT NULL, # 0 - by lvl; 1 - by TM; 2 - by HM
        level int NOT NULL, # level or TM/HM id

        Primary key (species_id, move_id, learning_by, level),
        UNIQUE INDEX (species_id, move_id, learning_by, level),
        Foreign Key (species_id) References pokespecies(id),
        Foreign Key (move_id) References move(id)
        );     
        
        CREATE TABLE states (
        id int NOT NULL PRIMARY KEY,
        name varchar(255) CHARACTER SET utf8 NOT NULL
        );
        """)
