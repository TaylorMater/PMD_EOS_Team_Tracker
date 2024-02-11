-- Create Dex_Reference
CREATE TABLE dex_reference (
  pokedex_num INT PRIMARY KEY,
  name VARCHAR(30) NOT NULL,
  iq_group CHAR NOT NULL,
  recruited BOOLEAN DEFAULT false,
);