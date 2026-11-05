import {
  createUserWithEmailAndPassword,
  onAuthStateChanged,
  signInWithEmailAndPassword,
  signOut as firebaseSignOut,
} from 'firebase/auth'
import { useEffect, useMemo, useState } from 'react'
import { AuthContext } from './auth-context.ts'
import { auth } from './firebase.ts'
import type { AuthContextValue } from './auth-context.ts'
import type { User } from 'firebase/auth'
import type { ReactNode } from 'react'

export function AuthProvider({ children }: { children: ReactNode }) {
  const [user, setUser] = useState<User | null>(null)
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    return onAuthStateChanged(auth, (nextUser) => {
      setUser(nextUser)
      setLoading(false)
    })
  }, [])

  const value = useMemo<AuthContextValue>(
    () => ({
      user,
      loading,
      signIn: async (email, password) => {
        await signInWithEmailAndPassword(auth, email, password)
      },
      signUp: async (email, password) => {
        await createUserWithEmailAndPassword(auth, email, password)
      },
      signOut: async () => {
        await firebaseSignOut(auth)
      },
    }),
    [user, loading],
  )

  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>
}
