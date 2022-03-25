-- This file can be run to create and insert values into our database, resetting it
--
-- Sets foreign keys on so foreign key restrictions are enforced
PRAGMA foreign_keys = ON;
-- Drops tables to reset the database
DROP TABLE IF EXISTS CoffeeTastes;
DROP TABLE IF EXISTS User;
DROP TABLE IF EXISTS RoastedCoffee;
DROP TABLE IF EXISTS Roastery;
DROP TABLE IF EXISTS Contains;
DROP TABLE IF EXISTS CoffeeBatch;
DROP TABLE IF EXISTS ProcessingMethod;
DROP TABLE IF EXISTS Grows;
DROP TABLE IF EXISTS CoffeeBean;
DROP TABLE IF EXISTS Farm;
DROP TABLE IF EXISTS Region;
DROP TABLE IF EXISTS Country;
--@Block
-- Create tables
-- Group members:
-- Markus Risa Vesetrud
-- Emma Eriksson Våge
-- -----------------------------------------------------
-- Table User 
-- -----------------------------------------------------
CREATE TABLE User (
    Email nvarchar(50),
    Password nvarchar(50),
    FullName nvarchar(50),
    PRIMARY KEY (Email)
);
-- -----------------------------------------------------
-- Table CoffeeTastes
-- -----------------------------------------------------
CREATE TABLE CoffeeTastes (
    TasteID INTEGER PRIMARY KEY,
    Email nvarchar(50) NOT NULL,
    CoffeeName nvarchar(50) NOT NULL,
    -- We would like to add a UNIQUE CONSTRAINT on CoffeeName and Roastery.name
    -- But those are in different tables, so we will do it on the application level instead
    RoasteryID int NOT NULL,
    Points tinyint CHECK (
        Points >= 0
        AND Points <= 10
    ),
    Notes nvarchar(1000),
    Date SMALLDATETIME,
    FOREIGN KEY (Email) REFERENCES User(Email) ON UPDATE CASCADE,
    FOREIGN KEY (CoffeeName, RoasteryID) REFERENCES RoastedCoffee(CoffeeName, RoasteryID) ON UPDATE CASCADE
);
-- -----------------------------------------------------
-- Table Roastery
-- -----------------------------------------------------
CREATE TABLE Roastery (
    RoasteryID INTEGER PRIMARY KEY,
    Name nvarchar(50),
    Country nvarchar(50),
    Region nvarchar(50),
    FOREIGN KEY (Country) REFERENCES Country(Country),
    FOREIGN KEY (Region) REFERENCES Region(Region)
);
-- -----------------------------------------------------
-- Table RoastedCoffee
-- -----------------------------------------------------
CREATE TABLE RoastedCoffee (
    CoffeeName nvarchar(50),
    RoasteryID int,
    BatchID int NOT NULL,
    -- The RoastDegree is stored as 1, 2, or 3
    -- 1 corresponds to "light"
    -- 2 corresponds to "medium"
    -- 3 corresponds to "dark"
    RoastDegree tinyint CHECK (
        RoastDegree >= 1
        AND RoastDegree <= 3
    ),
    RoastDate DATE,
    Description nvarchar(1000),
    PricePerKilo int,
    PRIMARY KEY (CoffeeName, RoasteryID),
    FOREIGN KEY (RoasteryID) REFERENCES Roastery(RoasteryID) ON DELETE CASCADE,
    FOREIGN KEY (BatchID) REFERENCES CoffeeBatch(BatchID)
);
-- -----------------------------------------------------
-- Table CoffeeBatch
-- -----------------------------------------------------
CREATE TABLE CoffeeBatch (
    BatchID INTEGER PRIMARY KEY,
    FarmID int NOT NULL,
    MethodName nvarchar(50) NOT NULL,
    HarvestYear int,
    PricePaidToFarm int,
    FOREIGN KEY (FarmID) REFERENCES Farm(FarmID),
    FOREIGN KEY (MethodName) REFERENCES ProcessingMethod(MethodName) ON UPDATE CASCADE
);
-- -----------------------------------------------------
-- Table ProcessingMethod 
-- -----------------------------------------------------
CREATE TABLE ProcessingMethod (
    MethodName nvarchar(50),
    Description nvarchar(1000),
    PRIMARY KEY (MethodName)
);
-- -----------------------------------------------------
-- Table CoffeeBean 
-- -----------------------------------------------------
CREATE TABLE CoffeeBean (
    BeanID INTEGER PRIMARY KEY,
    Name nvarchar(50),
    -- The Species is stored as 1, 2, 3, or 4 to save space
    -- 1 corresponds to "coffea"
    -- 2 corresponds to "arabica"
    -- 3 corresponds to "coffea robusta"
    -- 4 corresponds to "coffea liberica"
    Species tinyint CHECK (
        Species >= 1
        AND Species <= 4
    )
);
-- -----------------------------------------------------
-- Table Farm
-- -----------------------------------------------------
CREATE TABLE Farm (
    FarmID INTEGER PRIMARY KEY,
    Country nvarchar(50) NOT NULL,
    Region nvarchar(50) NOT NULL,
    Name nvarchar(50),
    MetersAboveSea int,
    FOREIGN KEY (Region) REFERENCES Region(Region),
    FOREIGN KEY (Country) REFERENCES Country(Country)
);
-- -----------------------------------------------------
-- Table Country 
-- -----------------------------------------------------
CREATE TABLE Country (Country nvarchar(50) PRIMARY KEY);
-- -----------------------------------------------------
-- Table Region 
-- -----------------------------------------------------
CREATE TABLE Region (Region nvarchar(50) PRIMARY KEY);
-- -----------------------------------------------------
-- Table Contains
-- -----------------------------------------------------
CREATE TABLE Contains (
    BatchID int,
    BeanID int,
    PRIMARY KEY (BatchID, BeanID),
    FOREIGN KEY (BatchID) REFERENCES CoffeeBatch(BatchID),
    FOREIGN KEY (BeanID) REFERENCES CoffeeBean(BeanID)
);
-- -----------------------------------------------------
-- Table Grows
-- -----------------------------------------------------
CREATE TABLE Grows (
    FarmID int,
    BeanID int,
    PRIMARY KEY (FarmID, BeanID),
    FOREIGN KEY (FarmID) REFERENCES Farm(FarmID),
    FOREIGN KEY (BeanID) REFERENCES CoffeeBean(BeanID)
);
-- -----------------------------------------------------
-- Inserting values
-- -----------------------------------------------------
INSERT INTO User (Email, Password, FullName)
VALUES (
        "ola.nordman@gmail.com",
        "Password123",
        "Ola Nordman"
    ),
    (
        "karl.karlsen@hotmail.com",
        "paris2022",
        "Karl Karlsen"
    ),
    (
        "maria.olsen@gmail.com",
        "qwerty42",
        "Maria Olsen"
    ),
    (
        "rektor@ntnu.no",
        "ntnuerbest",
        "Anne Borg"
    ),
    (
        "oskar@eriksen.no",
        "Pkf94RIFfz!",
        "Oskar Eriksen"
    );
INSERT INTO Country (Country)
VALUES ("El Salvador"),
    ("Italy"),
    ("Costa Rica"),
    ("South Africa"),
    ("Norway");
INSERT INTO Region (Region)
VALUES ("Santa Ana"),
    ("Bergamo"),
    ("Tarrazu"),
    ("Cape Town"),
    ("Trondheim"),
    ("Oslo");
INSERT INTO Roastery (Name, Country, Region)
VALUES ("Jacobsen & Svart", "Norway", "Trondheim"),
    ("Jacobsen & Svart", "Norway", "Oslo"),
    ("Barbarian Brewing Company", "Italy", "Bergamo"),
    ("The Whole Bean", "South Africa", "Cape Town"),
    ("Mocha Madness", "Costa Rica", "Tarrazu"),
    ("Steamed Beans", "Norway", "Trondheim");
INSERT INTO Farm (Country, Region, Name, MetersAboveSea)
VALUES (
        "El Salvador",
        "Santa Ana",
        "Nombre de Dios",
        1500
    ),
    (
        "Italy",
        "Bergamo",
        "Italian coffee farmers",
        300
    );
INSERT INTO ProcessingMethod (MethodName, Description)
VALUES ("Natural", "Do nothing basically"),
    ("Washed", "Wash all the beans"),
    (
        "Wet-hulled",
        "Hull and husk is removed at a greater moisture level"
    );
INSERT INTO CoffeeBean (Name, Species)
VALUES ("Bourbon", 1),
    ("Mocha", 1),
    ("Fancy Coffee cultivar", 3),
    ("Java", 2);
INSERT INTO CoffeeBatch (
        FarmID,
        MethodName,
        HarvestYear,
        PricePaidToFarm
    )
VALUES (1, "Natural", 2021, 8),
    (1, "Washed", 2020, 11),
    (2, "Wet-hulled", 2021, 7);
INSERT INTO RoastedCoffee (
        CoffeeName,
        RoasteryID,
        BatchID,
        RoastDegree,
        RoastDate,
        Description,
        PricePerKilo
    )
VALUES (
        "Vinterkaffe 2022",
        1,
        1,
        2,
        "2022-01-22",
        "A tasty and complex coffee for polar nights",
        600
    ),
    (
        "Vinterkaffe 2022",
        2,
        1,
        3,
        "2021-10-13",
        "A dark and spicy coffee roast",
        700
    ),
    (
        "Plan del Hoyo",
        3,
        2,
        2,
        "2022-02-23",
        "Tastes of strawberry and apricot",
        750
    ),
    -- This coffee is not tasted at all, but should still be findable for user story 4 and 5
    (
        "Ratnagiri Honey",
        4,
        3,
        1,
        "2022-01-05",
        "Tastes of aromatic apples and brown sugar",
        890
    );
INSERT INTO CoffeeTastes (
        Email,
        CoffeeName,
        RoasteryID,
        Points,
        Notes,
        Date
    )
VALUES (
        "ola.nordman@gmail.com",
        "Vinterkaffe 2022",
        1,
        10,
        "Wow an odyssey for the taste buds: citrus peel, milk chocolate, apricot!",
        "2022-03-14 12:00"
    ),
    (
        "ola.nordman@gmail.com",
        "Vinterkaffe 2022",
        1,
        9,
        "Exelent!",
        "2022-03-14 12:00"
    ),
    -- The following taste is for a different coffee than the one above (different RoasteryID)
    (
        "ola.nordman@gmail.com",
        "Vinterkaffe 2022",
        2,
        7,
        "The darker roast does note quite suit me",
        "2022-03-14 12:00"
    ),
    (
        "ola.nordman@gmail.com",
        "Plan del Hoyo",
        3,
        8,
        "You can really feel the strawberry!",
        "2022-03-14 12:00"
    ),
    (
        "maria.olsen@gmail.com",
        "Plan del Hoyo",
        3,
        7,
        "",
        "2022-03-14 12:00"
    ),
    -- Note how the following taste is registered in 2019 and therefore should not be taken into account by user story 2
    (
        "maria.olsen@gmail.com",
        "Vinterkaffe 2022",
        1,
        5,
        "Mediocre, just mediocre",
        "2019-03-14 12:00"
    ),
    (
        "oskar@eriksen.no",
        "Plan del Hoyo",
        3,
        4,
        "As expected",
        "2022-03-14 12:00"
    );
INSERT INTO Contains (BatchID, BeanID)
VALUES (1, 1),
    (1, 2),
    (2, 2),
    (3, 1);
INSERT INTO Grows (FarmID, BeanID)
VALUES (1, 1),
    (2, 1),
    (1, 2),
    (1, 3);
--@Block
-- Display every value
SELECT *
FROM User;
SELECT *
FROM Roastery;
SELECT *
FROM Country;
SELECT *
FROM Region;
SELECT *
FROM Farm;
SELECT *
FROM ProcessingMethod;
SELECT *
FROM CoffeeBean;
SELECT *
FROM CoffeeBatch;
SELECT *
FROM RoastedCoffee;
SELECT *
FROM CoffeeTastes;
SELECT *
FROM Grows;
SELECT *
FROM Contains;