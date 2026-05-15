module Main where

class Printable a where
  printable :: a -> String

instance Printable Bool where
  printable True = "yes"
  printable False = "no"

main :: IO ()
main = putStrLn (printable True)
