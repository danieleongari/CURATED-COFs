using CSV, DataFrames, Logging, Xtals

rc[:paths][:crystals] = "cifs"

xtal_names = readlines("./bond_anomalies.txt")
discarded_names = String.(CSV.read("cof-discarded.csv", DataFrame)[:, "CURATED-COFs ID"])

if isdir("reports")
    rm("reports", recursive=true, force=true)
end


function left_join(left::Vector{String}, right::Vector{String})::Vector{String}
    in_both = [l ∈ right for l in left]
    return left[.! in_both]
end


# only structures that cannot be fixed by optimization (based on manual inspection of COFs found by xtals_test1.jl)
problematic = left_join(xtal_names[[4, 36, 48, 50, 56, 59, 60]], discarded_names)
fixed = ["16056N2.cif", "20340N2.cif", "20670N3.cif", "21021N2.cif", "21192N2.cif", "21392N2.cif"]
problematic = left_join(problematic, fixed)


function run_report(names::Vector{String})
    dir = joinpath(pwd(), "reports")
    if !isdirpath(dir)
        mkpath(dir)
    end
    for name in names
        with_logger(SimpleLogger(open(joinpath(dir, name*".txt"), "w"))) do
            @assert !infer_bonds!(Crystal(name, convert_to_p1=false), true)
        end
    end
end


run_report(problematic)
