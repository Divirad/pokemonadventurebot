
def add_shop(cursor):
    cursor.execute("""
    INSERT INTO shop(name, price, productdescription, effect, effectvalue) 
        VALUES
        ('Pokéball', 200, 'Catches Pokémon', 0, NULL), 
        ('Greatball', 600, 'Greater chance than a Pokéball.', 0, NULL),
        ('Ultraball', 1200, 'Greater chance than a Great Ball.', 0, NULL),
        ('Masterball', 10000000, 'Always catches Pokemon.', 0, NULL),
        ('Potion', 300, 'Restores 20HP.', 1, 20),
        ('Super-Potion', 700, 'Restores 50HP.', 1, 50), 
        ('Hyper-Potion', 1200, 'Restores 200HP.', 1, 200),
        ('Max-Potion', 2500, 'Restores all HP.', 2, NULL),
        ('Full-Restore', 3000, 'Restores HP & status ailments.', 3, NULL)
        ;
    """)
    print("Added Shop, Items and Prices")
    pass


def fill_tables(cursor):
    add_shop(cursor)
