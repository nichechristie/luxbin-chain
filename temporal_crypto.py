
import hashlib
import time

class LuxbinTemporalCrypto:
    def __init__(self):
        self.keyLifetime = 24 * 60 * 60 * 1000  # 24 hours
        self.currentKey = None
        self.keyExpiry = None
        
    def generateTemporalKey(self):
        now = int(time.time() * 1000)
        timeWindow = now // (60 * 1000) * (60 * 1000)
        seed = f'luxbin-temporal-{timeWindow}'
        self.currentKey = hashlib.sha256(seed.encode()).hexdigest()[:16]
        self.keyExpiry = now + self.keyLifetime
        return self.currentKey
        
    def isKeyValid(self, key):
        return key == self.currentKey and time.time() * 1000 < self.keyExpiry
        
    def getTimeRemaining(self):
        if not self.keyExpiry:
            return 0
        return max(0, int((self.keyExpiry - time.time() * 1000) / 1000))
        
    def getKeyStatus(self):
        return {
            'currentKey': self.currentKey[:8] + '...' if self.currentKey else None,
            'timeRemaining': self.getTimeRemaining(),
            'isValid': self.currentKey and self.isKeyValid(self.currentKey)
        }
        
    def renewKey(self):
        return self.generateTemporalKey()
