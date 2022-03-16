-- Sets foreign keys on so foreign key restrictions are enforced
PRAGMA foreign_keys = ON;
-- Group members:
-- Markus Risa Vesetrud
-- Emma Erikson Våge
CREATE TABLE User (
    Email nvarchar(50),
    Password nvarchar(50),
    FullName nvarchar(50),
    PRIMARY KEY (Email)
);
CREATE TABLE CoffeeTastes (
    TasteID INTEGER PRIMARY KEY,
    Email nvarchar(50) NOT NULL,
    CoffeeName nvarchar(50) NOT NULL,
    RoasteryID int NOT NULL,
    Points tinyint CHECK (
        Points >= 0
        AND Points <= 10
    ),
    Notes nvarchar(1000),
    Date date,
    FOREIGN KEY (Email) REFERENCES User(Email),
    FOREIGN KEY (CoffeeName, RoasteryID) REFERENCES RoastedCoffee(CoffeeName, RoasteryID)
);
CREATE TABLE Roastery (
    RoasteryID INTEGER PRIMARY KEY,
    Name nvarchar(50)
);
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
    RoastDate date,
    Description nvarchar(1000),
    PricePerKilo int,
    PRIMARY KEY (CoffeeName, RoasteryID),
    FOREIGN KEY (RoasteryID) REFERENCES Roastery(RoasteryID) ON DELETE CASCADE,
    FOREIGN KEY (BatchID) REFERENCES CoffeeBatch(BatchID)
);
CREATE TABLE CoffeeBatch (
    BatchID INTEGER PRIMARY KEY,
    FarmID int NOT NULL,
    MethodName nvarchar(50) NOT NULL,
    HarvestYear int,
    PricePaidToFarm int,
    FOREIGN KEY (FarmID) REFERENCES Farm(FarmID),
    FOREIGN KEY (MethodName) REFERENCES ProcessingMethod(MethodName)
);
CREATE TABLE ProcessingMethod (
    MethodName nvarchar(50),
    Description nvarchar(1000),
    PRIMARY KEY (MethodName)
);
CREATE TABLE CoffeeBean (
    BeanID INTEGER PRIMARY KEY,
    Name nvarchar(50),
    Species nvarchar(20) CHECK (
        Species = "coffea"
        OR Species = "arabica"
        OR Species = "coffea robusta"
        OR Species = "coffea liberica"
    )
);
CREATE TABLE Farm (
    FarmID INTEGER PRIMARY KEY,
    LocationID int NOT NULL,
    Name nvarchar(50),
    MetersAboveSea int,
    FOREIGN KEY (LocationID) REFERENCES Location(LocationID)
);
CREATE TABLE Location (
    LocationID INTEGER PRIMARY KEY,
    Country nvarchar(50),
    Region nvarchar(50)
);
CREATE TABLE Contains (
    BatchID int,
    BeanID int,
    PRIMARY KEY (BatchID, BeanID),
    FOREIGN KEY (BatchID) REFERENCES CoffeeBatch(BatchID),
    FOREIGN KEY (BeanID) REFERENCES CoffeeBean(BeanID)
);
CREATE TABLE Grows (
    FarmID int,
    BeanID int,
    PRIMARY KEY (FarmID, BeanID),
    FOREIGN KEY (FarmID) REFERENCES Farm(FarmID),
    FOREIGN KEY (BeanID) REFERENCES CoffeeBean(BeanID)
);