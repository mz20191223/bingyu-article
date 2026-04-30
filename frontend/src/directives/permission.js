import { hasPerm } from '@/utils/permission'

export default {
  install(app) {
    app.directive('perm', {
      mounted(el, binding) {
        const permission = binding.value
        if (permission && !hasPerm(permission)) {
          el.style.display = 'none'
        }
      }
    })
  }
}