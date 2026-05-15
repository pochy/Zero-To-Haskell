module Main where

wrapMaybe :: a -> Maybe a
wrapMaybe = Just

main :: IO ()
main = print (wrapMaybe "kind * -> * の例")
