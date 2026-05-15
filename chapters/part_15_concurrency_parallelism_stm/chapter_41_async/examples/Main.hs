module Main where

import Control.Concurrent

main :: IO ()
main = do
  done <- newEmptyMVar
  _ <- forkIO (putMVar done "finished")
  takeMVar done >>= putStrLn
