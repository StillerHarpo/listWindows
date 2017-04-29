module WindowKey(
    getKeyComp
    Window
    )
    where

newtype Key = String 

newtype Window = String

-- | get a key-combination for each window
getKeyComp :: [Window] -> [(Window,Key)] 
getKeyComp w = getKeyCompKeys keys

-- | keys to chose the windows
keys :: [Key] 
keys = ["f","j","d","k","s","l","a"]


-- | get a key-combination for each window
-- with keys to generate the combination
getKeyCompKeys :: [Window] -> [Keys] -> [(Window,Key)] 
getKeyComp w k
  | small = zip w k
  | otherwise = getKeyComp (catesian k)
 where
     isSmall = length w < length k

-- | The Cartesian product for 2 strings with 
-- string-concatenation
cartesian :: [String] -> [String]
cartesian xs = [x++y | x <- xs, y <- xs]
