PRAGMA foreign_keys = ON;
CREATE TABLE User (
    Email nvarchar(50),
    Password nvarchar(50),
    FullName nvarchar(50),
    PRIMARY KEY (Email)
);
CREATE TABLE CoffeeTastes (
    TasteID int,
    Email nvarchar(50) NOT NULL,
    CoffeeName nvarchar(50) NOT NULL,
    RoasteryID int NOT NULL,
    Points tinyint CHECK (
        Points >= 0
        AND Points <= 10
    ),
    Notes text,
    Date date,
    PRIMARY KEY (TasteID),
    FOREIGN KEY (Email) REFERENCES User(Email),
    FOREIGN KEY (CoffeeName, RoasteryID) REFERENCES RoastedCoffee(CoffeeName, RoasteryID)
);
CREATE TABLE Roastery (
    RoasteryID int,
    Name nvarchar(50),
    PRIMARY KEY (RoasteryID)
);
CREATE TABLE RoastedCoffee (
    CoffeeName nvarchar(50),
    RoasteryID int,
    BatchID int NOT NULL,
    RoastDegree nvarchar(30) CHECK (
        RoastDegree = 'light'
        OR RoastDegree = 'medium'
        OR RoastDegree = 'dark'
    ),
    RoastDate date,
    Description text,
    PricePerKilo int,
    PRIMARY KEY (CoffeeName, RoasteryID),
    FOREIGN KEY (RoasteryID) REFERENCES Roastery(RoasteryID) ON DELETE CASCADE,
    FOREIGN KEY (BatchID) REFERENCES CoffeeBatch(BatchID)
);
CREATE TABLE CoffeeBatch (
    BatchID int,
    FarmID int NOT NULL,
    MethodName nvarchar(50) NOT NULL,
    HarvestYear int,
    PricePaidToFarm int,
    PRIMARY KEY (BatchID),
    FOREIGN KEY (FarmID) REFERENCES Farm(FarmID),
    FOREIGN KEY (MethodName) REFERENCES ProcessingMethod(MethodName)
);
CREATE TABLE ProcessingMethod (
    MethodName nvarchar(50),
    Description text,
    PRIMARY KEY (MethodName)
);
CREATE TABLE CoffeeBean (
    BeanID int,
    Name nvarchar(50),
    Species nvarchar(20) CHECK (
        Species = "coffea"
        OR Species = "arabica"
        OR Species = "coffea robusta"
        OR Species = "coffea liberica"
    ),
    PRIMARY KEY (BeanID)
);
CREATE TABLE Farm (
    FarmID int,
    LocationID int NOT NULL,
    Name nvarchar(50),
    MetersAboveSea int,
    PRIMARY KEY (FarmID),
    FOREIGN KEY (LocationID) REFERENCES Location(LocationID)
);
CREATE TABLE Location (
    LocationID int,
    Country nvarchar(50),
    Region nvarchar(50),
    PRIMARY KEY (LocationID)
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