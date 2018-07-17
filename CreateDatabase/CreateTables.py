
def create_tables(cursor):

    cursor.execute("""
    
        CREATE TABLE shop (
        id int NOT NULL PRIMARY KEY AUTO_INCREMENT,
        name varchar(30) NOT NULL,
        price int NOT NULL,
        discount int DEFAULT 0 NOT NULL,
        productdescription text NOT NULL,
        effect int DEFAULT 0,
        effectvalue int DEFAULT 0
        );
        
        CREATE TABLE learned_move (
        id int NOT NULL PRIMARY KEY AUTO_INCREMENT,
        move_id int NOT NULL,
        currentap int NOT NULL,
        blocked boolean NOT NULL,
        blockedforrounds int NOT NULL,

        Foreign Key (move_id) References move(id)
        );
        
        # describes an pokemon owned by a trainer
        CREATE TABLE pokemon (
        id int NOT NULL PRIMARY KEY AUTO_INCREMENT,
        ownedby int,
        originaltrainer int,
        species_id int NOT NULL,
        name varchar(255) CHARACTER SET utf8 NOT NULL,
        teamnr int,
        currenthp int NOT NULL,
        current_status int NOT NULL,
        exp int DEFAULT 0 NOT NULL,
        level int DEFAULT 1 NOT NULL,
        hp_exp int DEFAULT 0 NOT NULL,
        attack_exp int DEFAULT 0 NOT NULL,
        defense_exp int DEFAULT 0 NOT NULL,
        special_exp int DEFAULT 0 NOT NULL,
        speed_exp int DEFAULT 0 NOT NULL,
        hp_dv int NOT NULL,
        attack_dv int NOT NULL,
        defense_dv int NOT NULL,
        special_dv int NOT NULL,
        speed_dv int NOT NULL,
        gender char(1) NOT NULL,    # 'm', 'f' or 'n'
        move0 int,
        move1 int,
        move2 int,
        move3 int,

        Foreign key (species_id) References pokespecies(id),
        Foreign key (move0) References learned_move(id),
        Foreign key (move1) References learned_move(id),
        Foreign key (move2) References learned_move(id),
        Foreign key (move3) References learned_move(id),
        Foreign key (current_status) References states(id)
        );
        
        # something like an arena
        # for every pokemonfight
        CREATE TABLE pokemonfight (
        id int NOT NULL PRIMARY KEY AUTO_INCREMENT,
        wildPokemon int NOT NULL,
        trainerPokemon int NOT NULL,
        wild_attack int NOT NULL,
        wild_defense int NOT NULL,
        wild_special int NOT NULL,
        wild_speed int NOT NULL,
        trainer_attack int NOT NULL,
        trainer_defense int NOT NULL,
        trainer_special int NOT NULL,
        trainer_speed int NOT NULL,
        wild_attack_stage int NOT NULL,
        wild_defense_stage int NOT NULL,
        wild_special_stage int NOT NULL,
        wild_speed_stage int NOT NULL,
        trainer_attack_stage int NOT NULL,
        trainer_defense_stage int NOT NULL,
        trainer_special_stage int NOT NULL,
        trainer_speed_stage int NOT NULL,

        Foreign Key (wildPokemon) References pokemon(id),
        Foreign Key (trainerPokemon) References pokemon(id)
        );

        # describes an user / a trainer
        CREATE TABLE trainer (
        id int NOT NULL PRIMARY KEY,
        menu_id int DEFAULT 0 NOT NULL,
        name varchar(255) NOT NULL,
        pokedollar int DEFAULT 0 NOT NULL,
        blocked boolean DEFAULT false NOT NULL,
        blocktimer datetime DEFAULT NULL ,
        registeredsince datetime NOT NULL,
        badges int DEFAULT 0 NOT NULL,
        fight int DEFAULT NULL,
        draws int DEFAULT 0 NOT NULL,
        wins int DEFAULT 0 NOT NULL,
        looses int DEFAULT 0 NOT NULL,
        lastcatched int DEFAULT NULL,
        game_pos_x int DEFAULT 1 NOT NULL,
        game_pos_y int DEFAULT 1 NOT NULL,
        game_location_id int DEFAULT 1 NOT NULL,
        
        Foreign Key (fight) References pokemonfight(id)
        );

        ALTER TABLE pokemon ADD (
        Foreign key (ownedby) References trainer(id),
        Foreign key (originaltrainer) References trainer(id)
        );
        
        # Describes an entry in the pokedex 
        CREATE TABLE pokedex (
        id int NOT NULL,
        trainerid int NOT NULL,

        Primary key (id, trainerid),
        UNIQUE INDEX (id, trainerid),

        Foreign key (id) References pokespecies(id),
        Foreign key (trainerid) References trainer(id)
        );
        
        # Describes the items a user owns
        CREATE TABLE user_item (
        id int NOT NUll,
        trainerid int NOT NULL,
        amount int DEFAULT 0 NOT NULL,
        
        PRIMARY KEY (id, trainerid),
        UNIQUE INDEX (id, trainerid),
        FOREIGN KEY (id) References shop(id),
        FOREIGN KEY (trainerid) References trainer(id)
        );
        
        CREATE TABLE daily(
        code varchar(8) NOT NULL PRIMARY KEY
        )
        """)
        
    print("Tables created")
