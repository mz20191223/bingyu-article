import { useUserStore } from '@/stores/user'

export function hasPerm(perm) {
  const userStore = useUserStore()
  const permissions = userStore.permissions || []
  return permissions.includes(perm)
}

export function hasAnyPerm(perms) {
  const userStore = useUserStore()
  const permissions = userStore.permissions || []
  return perms.some(perm => permissions.includes(perm))
}

export function hasAllPerms(perms) {
  const userStore = useUserStore()
  const permissions = userStore.permissions || []
  return perms.every(perm => permissions.includes(perm))
}