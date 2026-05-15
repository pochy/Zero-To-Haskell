{-# LANGUAGE RankNTypes #-}
module Main where

applyToBoth :: (forall a. a -> a) -> (Int, Bool)
applyToBoth f = (f 1, f True)

main :: IO ()
main = print (applyToBoth id)
