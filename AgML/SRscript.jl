import SymbolicRegression: SRRegressor
import MLJ: machine, fit!, predict, report

using DataFrames
using CSV
using LinearAlgebra
#Load data from modified_featuresv3.csv, first column is index
df = CSV.read("modified_featuresv4.csv", DataFrame, header=true, delim=',')
#the first 9 columns are X, the last column is Y
X = df[:,2:10]
Y =  df[:,11]
#multiply the first and second column of X and discard the original columns
X = hcat(X, X[:,1].*X[:,2])
X = X[:,3:10]
print(X)
#print the first 5 rows of X and Y
println(X[1:5,:])
println(Y[1:5])

#convert dataframe into array
X = Matrix(X)
#combine first and second column of X multiplying them and discard the original columns
#X = hcat(X, X[:,1].*X[:,2])
#print(X[1:5,:])
#X = X[:,3:10]
print(X[1:5,:])
Y = Vector( Y)
#transpose X


model = SRRegressor(
    niterations=300,
    binary_operators=[+, -, *,/],
    unary_operators=[exp, log, sqrt, square,cube],
)
mach = machine(model, X, Y)

fit!(mach)
report(mach)