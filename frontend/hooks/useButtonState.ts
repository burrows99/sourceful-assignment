/**
 * useButtonState Hook
 * 
 * Custom hook to manage button state logic including:
 * - Feature availability based on credits
 * - Button text (with override for low credits)
 * - Icon positioning
 * - Disabled state calculation
 */

import { useAuth } from '@/lib/auth-context';
import type { PromptSubmitButton } from '@/components/ui/SubmitButton';

export function useButtonState(promptSubmitButton?: PromptSubmitButton) {
  const { isAuthenticated, credits } = useAuth();
  
  if (!promptSubmitButton) {
    return {
      buttonText: 'Start',
      iconSide: 'right' as const,
      isDisabled: false,
      showCreditBadge: false,
      credits: 0,
    };
  }
  
  // Get feature availability result if available
  const featureAvailable = promptSubmitButton.isFeatureAvailable?.(credits) ?? null;
  
  // Determine final state based on auth and feature availability
  const finalState = featureAvailable !== null ? featureAvailable : isAuthenticated;
  
  // Calculate button text with override
  const baseButtonText = promptSubmitButton.buttonText || 'Start';
  const buttonTextOverride = promptSubmitButton.buttonTextOverrideIfLowCredits;
  const buttonText = (featureAvailable === false && buttonTextOverride) 
    ? buttonTextOverride 
    : baseButtonText;
  
  // Calculate icon side
  const iconSide = promptSubmitButton.iconSide || (finalState ? 'right' : 'left');
  
  // Calculate disabled state
  const isDisabled = 
    promptSubmitButton.forceDisabled || 
    (promptSubmitButton.shouldToggleDisabled && !isAuthenticated) || 
    (featureAvailable !== null && !featureAvailable);
  
  // Show credit badge when feature availability check exists
  const showCreditBadge = !!promptSubmitButton.isFeatureAvailable;
  
  return {
    buttonText,
    iconSide,
    isDisabled,
    showCreditBadge,
    credits,
  };
}
