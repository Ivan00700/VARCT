def beautu_print_masses_V(massFuel1step, massFuel2step, rocket_mass):
    print("\t' \t\t\t[First and Second from file]")
    print("\n Fuel masses for stages got from Tsiolkovsky's and V got from Tsiolkovsky's to several stages\n")
    
    V = get_V(massFuel1step, massFuel2step)  # Предполагается, что эта функция определена где-то еще
    
    print("\t' " + lu_corner + print_line(75) + ru_corner)
    print("\t' " + strait)
    
    # Форматированный вывод
    print(f"M. rocket: {rocket_mass:.2f}")
    print(f"M. first stage: {massFuel1step:.2f}")
    print(f"M. second stage: {massFuel2step:.2f}")
    print(f"Velocity: {V:.2f}")
    
    print("\t' " + ls_trait + print_line(75) + rs_trait)
    print("\t' " + strait + f"{rocket_mass:<6} \t\t {massFuel1step:<{width}} \t\t {massFuel2step:<{width}} \t {V:<{width}}")
    print("\t' " + ld_corner + print_line(75) + rd_corner + "\n\n")
