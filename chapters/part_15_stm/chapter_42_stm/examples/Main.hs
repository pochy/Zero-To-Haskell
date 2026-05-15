module Main where

import Control.Concurrent.STM

main :: IO ()
main = do
  counter <- newTVarIO (0 :: Int)
  atomically (modifyTVar' counter (+1))
  readTVarIO counter >>= print
