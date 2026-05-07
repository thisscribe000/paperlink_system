import { customAlphabet } from 'nanoid'

const alphabet = '0123456789abcdefghijklmnopqrstuvwxyz'
export const generateId = customAlphabet(alphabet, 10)

export function generateSlug(length = 8): string {
  return customAlphabet(alphabet, length)()
}