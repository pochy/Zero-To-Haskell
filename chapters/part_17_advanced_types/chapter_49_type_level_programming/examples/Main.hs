{-# LANGUAGE DataKinds #-}
module Main where

data Visibility = Public | Private
newtype Document (v :: Visibility) = Document String deriving Show

main :: IO ()
main = print (Document "guide" :: Document 'Public)
