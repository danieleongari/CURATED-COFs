using Logging, Xtals

rc[:paths][:crystals] = "cifs"

xtal_names = readlines("./bond_anomalies.txt")

bogus_C = xtal_names[[59]]
bogus_H = xtal_names[[2, 4, 11, 36, 48, 50, 51, 56, 57, 60, 63, 64]]
close_contacts = xtal_names[[1, 7, 16, 20, 23, 30, 32, 33, 37, 38, 39, 40, 41, 42, 44, 45, 46, 47]]
long_bonds = xtal_names[[3, 5, 19, 21, 25, 26, 27, 28, 29, 31, 34, 35, 43, 49, 52, 58, 61]]


function run_report(names::Vector{String}, label::String)
    dir = joinpath(pwd(), "reports", label)
    if !isdirpath(dir)
        mkpath(dir)
    end
    for name in names
        with_logger(SimpleLogger(open(joinpath(dir, name*".txt"), "w"))) do
            @assert !infer_bonds!(Crystal(name, convert_to_p1=false), true)
        end
    end
end


run_report(long_bonds, "long_bonds")
run_report(close_contacts, "close_contacts")
run_report(bogus_C, "bogus_C")
run_report(bogus_H, "bogus_H")
