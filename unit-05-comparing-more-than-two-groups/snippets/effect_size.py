# Step 5. Eta squared is this sample's share of the variance. Omega squared
# estimates the population's, and is the one to describe in words.
eta2 = m9.eta_squared(groups)
omega2 = m9.omega_squared(groups)

print(f"eta squared = {eta2:.3f}")
print(f"omega squared = {omega2:.3f} ({m9.interpret(omega2, 'eta2')})")
