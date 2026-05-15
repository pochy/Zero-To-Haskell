module Main where

-- 実際のFFIでは foreign import ccall を使う。
cBoundary :: Int -> Int
cBoundary n = n + 1

main :: IO ()
main = print (cBoundary 41)
