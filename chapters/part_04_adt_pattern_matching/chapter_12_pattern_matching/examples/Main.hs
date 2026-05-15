module Main where

data Status = Draft | Published String

label :: Status -> String
label Draft = "draft"
label (Published title) = "published: " ++ title

main :: IO ()
main = putStrLn (label (Published "Guide"))
