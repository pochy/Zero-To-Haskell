module Main where

data AppError = MissingName deriving Show
newtype Env = Env { defaultName :: String }

runApp :: Env -> Maybe String -> Either AppError String
runApp env input =
  Right ("Hello, " ++ maybe (defaultName env) id input)

main :: IO ()
main = print (runApp (Env "guest") Nothing)
