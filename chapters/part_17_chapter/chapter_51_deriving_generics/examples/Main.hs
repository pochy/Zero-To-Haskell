{-# LANGUAGE DeriveGeneric #-}
module Main where

import GHC.Generics (Generic)

data User = User String Int deriving (Show, Eq, Generic)

main :: IO ()
main = print (User "Ada" 36 == User "Ada" 36)
