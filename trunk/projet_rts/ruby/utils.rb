#
# Fonctions utilitaires
#
module Utils

	#
	# Compare a et b et renvoie la valeur la plus grande
	# Si a = b, renvoie a
	#
	def max(a,b)
		if a<b
			return b
		else
			return a
		end
	end

	#
	# Compare a et b et renvoie la valeur la plus petite
	# Si a = b, renvoie b
	#
	def min(a,b)
		if a<b
			return a
		else
			return b
		end
	end

end