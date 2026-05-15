module Main where

data AppError = NotFound | InvalidInput deriving Show

handle :: Maybe String -> Either AppError String
handle Nothing = Left NotFound
handle (Just "") = Left InvalidInput
handle (Just value) = Right ("ok: " ++ value)

main :: IO ()
main = print (handle (Just "request"))
