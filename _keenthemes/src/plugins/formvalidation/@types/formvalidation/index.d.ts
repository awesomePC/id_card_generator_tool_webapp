/**
 * FormValidation (https://formvalidation.io)
 * The best validation library for JavaScript
 * (c) 2013 - 2021 Nguyen Huu Phuoc <me@phuoc.ng>
 */

// Algorithms
// ----------

declare module 'formvalidation/algorithms/luhn' {
    function luhn(value: string): boolean;
    export = luhn;
}

declare module 'formvalidation/algorithms/mod11And10' {
    function mod11And10(value: string): boolean;
    export = mod11And10;
}

declare module 'formvalidation/algorithms/mod37And36' {
    function mod37And36(value: string, alphabet?: string): boolean;
    export = mod37And36;
}

declare module 'formvalidation/algorithms/mod97And10' {
    function mod97And10(value: string): boolean;
    export = mod97And10;
}

declare module 'formvalidation/algorithms/verhoeff' {
    function verhoeff(value: number[]): boolean;
    export = verhoeff;
}

// Core
// ----

declare namespace core {
    interface ValidatorOptions {
        enabled?: boolean;
        message?: string;
        [option: string]: unknown;
    }
    interface FieldOptions {
        selector?: string;
        validators: {
            [validatorName: string]: ValidatorOptions,
        };
    }
    interface FieldsOptions {
        [field: string]: FieldOptions;
    }
    interface Localization {
        [validator: string]: {
            default?: string,
        };
    }
    interface LocalizationMessage {
        [locale: string]: string;
    }
    type LocalizationMessageType =  LocalizationMessage | string;
    interface ValidateOptions {
        message?: string;
    }
    interface ValidateInput<T extends ValidateOptions, L extends Localization> {
        element?: HTMLElement;
        elements?: HTMLElement[];
        field?: string;
        options?: T;
        l10n?: L;
        value: string;
    }
    interface ValidateResult {
        message?: LocalizationMessageType;
        meta?: unknown;
        valid: boolean;
    }

    interface ValidateFunctionInterface<K extends ValidateOptions, T> {
        validate(input: ValidateInput<K, Localization>): T;
    }
    type ValidateFunction<K extends ValidateOptions> = ValidateFunctionInterface<K, ValidateResult | Promise<ValidateResult>>;

    class Core {
        constructor(form: HTMLElement, fields?: FieldsOptions);
        
        on(event: string, func: (...arg: unknown[]) => unknown): Core;
        off(event: string, func: (...arg: unknown[]) => unknown): Core;
        emit(event: string, ...args: unknown[]): Core;
        
        registerPlugin(name: string, plugin: Plugin<unknown>): Core;
        deregisterPlugin(name: string): Core;
        
        registerValidator(name: string, func: () => ValidateFunction<ValidateOptions>): Core;
        registerValidator<K extends ValidateOptions>(name: string, func: () => ValidateFunction<K>): Core;
        registerFilter(name: string, func: (...arg: unknown[]) => unknown): Core;
        deregisterFilter(name: string, func: (...arg: unknown[]) => unknown): Core;
        executeFilter<T>(name: string, defaultValue: T, args: unknown[]): T;
        
        addField(field: string, options?: FieldOptions): Core;
        removeField(field: string): Core;
        
        revalidateField(field: string): Promise<string>;
        validate(): Promise<string>;
        validateField(field: string): Promise<string>;
        validateElement(field: string, ele: HTMLElement): Promise<string>;
        executeValidator(field: string, ele: HTMLElement, v: string, opts: ValidatorOptions): Promise<string>;
        
        getElementValue(field: string, ele: HTMLElement, validator?: string): string;
        getElements(field: string): HTMLElement[];
        getFields(): FieldsOptions;
        getFormElement(): HTMLElement;
        getLocale(): string;
        getPlugin(name: string): Plugin<any>;
        
        updateFieldStatus(field: string, status: string, validator?: string): Core;
        updateElementStatus(field: string, ele: HTMLElement, status: string, validator?: string): Core;
        
        resetForm(reset?: boolean): Core;
        resetField(field: string, reset?: boolean): Core;

        disableValidator(field: string, validator?: string): Core;
        enableValidator(field: string, validator?: string): Core;
        updateValidatorOption(field: string, validator: string, name: string, value: unknown): Core;
        setFieldOptions(field: string, options: FieldOptions): Core;

        destroy(): Core;

        setLocale(locale: string, localization: Localization): Core;
    }

    class Plugin<T> {
        constructor(opts?: T);
        setCore(core: Core): Plugin<T>;
        install(): void;
        uninstall(): void;
    }
}

declare module 'formvalidation/core/Core' {
    interface Options {
        fields?: core.FieldsOptions;
        locale?: string;
        localization?: core.Localization;
        plugins?: {
            [name: string]: core.Plugin<unknown>,
        };
        init?(core: core.Core): void;
    }
    function formValidation(form: HTMLElement, options?: Options): core.Core;

    export = formValidation;
}

declare module 'formvalidation/core/Plugin' {
    export = core.Plugin;
}

// Plugins
// -------

declare module 'formvalidation/plugins/Alias' {
    interface AliasOptions {
        // Map the alias with defined validator name
        [alias: string]: string;
    }
    class Alias extends core.Plugin<AliasOptions> {
        constructor(opts?: AliasOptions);
    }
    export = Alias;
}

declare module 'formvalidation/plugins/Aria' {
    class Aria extends core.Plugin<{}> {
        constructor();
    }
    export = Aria;
}

declare module 'formvalidation/plugins/AutoFocus' {
    interface AutoFocusOptions {
        onPrefocus: (AutoFocusPrefocusEvent) => void;
    }
    interface AutoFocusPrefocusEvent {
        field: string;
        firstElement: HTMLElement;
    }
    class AutoFocus extends core.Plugin<AutoFocusOptions> {
        constructor(opts?: AutoFocusOptions);
    }
    export = AutoFocus;
}

declare module 'formvalidation/plugins/Declarative' {
    interface DeclarativeOptions {
        // Set it to `true` to enable the validators automatically based on the input type or particular HTML 5 attributes:
        //  -----------------+---------------------
        //  HTML 5 attribute | Equivalent validator
        //  -----------------+---------------------
        //  max="..."        | lessThan
        //  min="..."        | greaterThan
        //  maxlength="..."  | stringLength
        //  minlength="..."  | stringLength
        //  pattern="..."    | regexp
        //  required         | notEmpty
        //  type="color"     | color
        //  type="email"     | emailAddress
        //  type="range"     | between
        //  type="url"       | uri
        //  -----------------+---------------------
        // It's not enabled by default
        html5Input?: boolean;
        // The prefix of plugin declaration attributes. By default, it is set to `data-fvp-`
        pluginPrefix?: string;
        // The prefix of attributes. By default, it is set to `data-fv-`
        prefix?: string;
    }
    class Declarative extends core.Plugin<DeclarativeOptions> {
        constructor(opts?: DeclarativeOptions);
    }
    export = Declarative;
}

declare module 'formvalidation/plugins/DefaultSubmit' {
    class DefaultSubmit extends core.Plugin<{}> {
        constructor();
    }
    export = DefaultSubmit;
}

declare module 'formvalidation/plugins/Dependency' {
    interface DependencyOptions {
        [field: string]: string;
    }
    class Dependency extends core.Plugin<DependencyOptions> {
        constructor(opts: DependencyOptions);
    }
    export = Dependency;
}

declare module 'formvalidation/plugins/Excluded' {
    type ExcludedCallback = (field: string, element: HTMLElement, elements: HTMLElement[]) => boolean;
    interface ExcludedOptions {
        excluded: ExcludedCallback;
    }
    class Excluded extends core.Plugin<ExcludedOptions> {
        constructor(opts?: ExcludedOptions);
    }
    export = Excluded;
}

declare module 'formvalidation/plugins/FieldStatus' {
    interface FieldStatusOptions {
        onStatusChanged?: (areFieldsValid: boolean) => void;
    }
    class FieldStatus extends core.Plugin<FieldStatusOptions> {
        constructor(opts?: FieldStatusOptions);
    }
    export = FieldStatus;
}

declare module 'formvalidation/plugins/Icon' {
    interface IconOptions {
        invalid?: string;
        valid?: string;
        validating?: string;
        onPlaced?: (IconPlacedEvent) => void;
        onSet?: (IconSetEvent) => void;
    }
    interface IconPlacedEvent {
        element: HTMLElement;
        field: string;
        iconElement: HTMLElement;
        classes: IconOptions;
    }
    interface IconSetEvent {
        element: HTMLElement;
        field: string;
        status: string;
        iconElement: HTMLElement;
    }
    class Icon extends core.Plugin<IconOptions> {
        constructor(opts?: IconOptions);
    }
    export = Icon;
}

declare module 'formvalidation/plugins/InternationalTelephoneInput' {
    interface InternationalTelephoneInputOptions {
        autoPlaceholder?: string;
        field: string | string[];
        message: string;
        utilsScript?: string;
    }
    // See https://github.com/jackocnr/intl-tel-input#public-methods for more methods
    interface IntlTelInput {
        destroy(): void;
        getExtension(): string;
        getNumber(format?: number): string;
        getNumberType(): number;
        getValidationError(): number;
        isValidNumber(): boolean;
        setCountry(country: string): void;
        setNumber(number: string): void;
        setPlaceholderNumberType(numberType: string): void;
    }
    class InternationalTelephoneInput extends core.Plugin<InternationalTelephoneInputOptions> {
        constructor(opts?: InternationalTelephoneInputOptions);
        static INT_TEL_VALIDATOR: string;
        getIntTelInstance(field: string): IntlTelInput | null;
    }
    export = InternationalTelephoneInput;
}

declare module 'formvalidation/plugins/L10n' {
    interface LiteralMessage {
        [locale: string]: string;
    }
    type CallbackMessage = (field: string, validator: string) => LiteralMessage;
    interface L10nOptions {
        [field: string]: {
            [validator: string]: LiteralMessage | CallbackMessage,
        };
    }
    class L10n extends core.Plugin<L10nOptions> {
        constructor(opts?: L10nOptions);
    }
    export = L10n;
}

declare module 'formvalidation/plugins/Mailgun' {
    interface MailgunOptions {
        // The API key provided by Mailgun
        apiKey: string;
        // The field name that will be validated
        field: string;
        // Error message indicates the input is not valid
        message: string;
        // Show suggestion if the email is not valid
        suggestion?: boolean;
    }
    class Mailgun extends core.Plugin<MailgunOptions> {
        constructor(opts?: MailgunOptions);
    }
    export = Mailgun;
}

declare module 'formvalidation/plugins/MandatoryIcon' {
    interface MandatoryIconOptions {
        icon: string;
    }
    class MandatoryIcon extends core.Plugin<MandatoryIconOptions> {
        constructor(opts?: MandatoryIconOptions);
    }
    export = MandatoryIcon;
}

declare module 'formvalidation/plugins/PasswordStrength' {
    interface PasswordStrengthOptions {
        field: string;
        message: string;
        minimalScore: number;
        onValidated?: (valid: boolean, message: string, score: number) => void;
    }
    class PasswordStrength extends core.Plugin<PasswordStrengthOptions> {
        constructor(opts?: PasswordStrengthOptions);
        static PASSWORD_STRENGTH_VALIDATOR: string;
    }
    export = PasswordStrength;
}

declare module 'formvalidation/plugins/Message' {
    type ContainerCallback = (field: string, element: HTMLElement) => HTMLElement;
    interface MessageOptions {
        clazz?: string;
        container?: string | ContainerCallback;
    }
    class Message extends core.Plugin<MessageOptions> {
        constructor(opts?: MessageOptions);
        static getClosestContainer(element: HTMLElement, upper: HTMLElement, pattern: RegExp): HTMLElement;
    }
    export = Message;
}

declare module 'formvalidation/plugins/Recaptcha' {
    interface RecaptchaOptions {
        // The ID of element showing the captcha
        element: string;
        // The language code defined by reCAPTCHA
        // See https://developers.google.com/recaptcha/docs/language
        language?: string;
        // The invalid message that will be shown in case the captcha is not valid
        // You don't need to define it if the back-end URL above returns the message
        message: string;
        // The site key provided by Google
        siteKey: string;
        backendVerificationUrl?: string;
    
        // The size of widget. It can be 'compact', 'normal' (default), or 'invisible'
        size?: string;
    
        // reCAPTCHA widget option (size can be 'compact' or 'normal')
        // See https://developers.google.com/recaptcha/docs/display
    
        // The theme name provided by Google. It can be light (default), dark
        theme?: string;
    
        // Invisible reCAPTCHA
        // See https://developers.google.com/recaptcha/docs/invisible
        // The position of reCAPTCHA. Can be 'bottomright' (default), 'bottomleft', 'inline'
        badge?: string;
    }
    class Recaptcha extends core.Plugin<RecaptchaOptions> {
        constructor(opts?: RecaptchaOptions);
        static CAPTCHA_FIELD: string;
    }
    export = Recaptcha;
}

declare module 'formvalidation/plugins/Recaptcha3' {
    interface Recaptcha3Options {
        // The ID of element showing the captcha error
        element: string;
        // The language code defined by reCAPTCHA
        // See https://developers.google.com/recaptcha/docs/language
        language?: string;
        // Minimum score, between 0 and 1
        minimumScore?: number;
        // The invalid message that will be shown in case the captcha is not valid
        // You don't need to define it if the back-end URL above returns the message
        message: string;
        // The site key provided by Google
        siteKey: string;
        backendVerificationUrl: string;
        action: string;
    }
    class Recaptcha3 extends core.Plugin<Recaptcha3Options> {
        constructor(opts?: Recaptcha3Options);
        static CAPTCHA_FIELD: string;
    }
    export = Recaptcha3;
}

declare module 'formvalidation/plugins/Recaptcha3Token' {
    interface Recaptcha3TokenOptions {
        action: string;
        hiddenTokenName: string;
        language?: string;
        siteKey: string;
    }
    class Recaptcha3Token extends core.Plugin<Recaptcha3TokenOptions> {
        constructor(opts?: Recaptcha3TokenOptions);
    }
    export = Recaptcha3Token;
}

declare module 'formvalidation/plugins/Sequence' {
    interface SequenceOptions {
        enabled: boolean | { [field: string]: boolean };
    }
    class Sequence extends core.Plugin<SequenceOptions> {
        constructor(opts?: SequenceOptions);
    }
    export = Sequence;
}

declare module 'formvalidation/plugins/StartEndDate' {
    interface StartEndDateOptions {
        format: string;
        startDate: {
            field: string;
            message: string;
        };
        endDate: {
            field: string;
            message: string;
        };
    }
    class StartEndDate extends core.Plugin<StartEndDateOptions> {
        constructor(opts?: StartEndDateOptions);
    }
    export = StartEndDate;
}

declare module 'formvalidation/plugins/SubmitButton' {
    interface SubmitButtonOptions {
        aspNetButton?: boolean;
        // Allow to query the submit button(s)
        // It's useful in case the submit button is outside of form
        buttons?: (form: HTMLFormElement) => Element[];
    }
    class SubmitButton extends core.Plugin<SubmitButtonOptions> {
        constructor(opts?: SubmitButtonOptions);
    }
    export = SubmitButton;
}

declare module 'formvalidation/plugins/Tooltip' {
    interface TooltipOptions {
        placement: string;
        trigger: string;
    }
    class Tooltip extends core.Plugin<TooltipOptions> {
        constructor(opts?: TooltipOptions);
    }
    export = Tooltip;
}

declare module 'formvalidation/plugins/Transformer' {
    interface TransformerOptions {
        [field: string]: {
            [validator: string]: (field: string, element: HTMLElement, validator: string) => string,
        };
    }
    class Transformer extends core.Plugin<TransformerOptions> {
        constructor(opts?: TransformerOptions);
    }
    export = Transformer;
}

declare module 'formvalidation/plugins/Trigger' {
    interface TriggerOptions {
        delay?: number | {
            [field: string]: number,
        };
        event: string | {
            [field: string]: boolean | string,
        };
        // Only perform the validation if the field value exceed this number of characters
        threshold?: number | {
            [field: string]: number,
        };
    }
    class Trigger extends core.Plugin<TriggerOptions> {
        constructor(opts?: TriggerOptions);
    }
    export = Trigger;
}

declare module 'formvalidation/plugins/Wizard' {
    interface WizardOptions {
        stepSelector: string;
        prevButton: string | HTMLElement;
        nextButton: string | HTMLElement;
        onStepActive?: (WizardStepEvent) => void;
        onStepInvalid?: (WizardStepEvent) => void;
        onStepValid?: (WizardStepEvent) => void;
        onValid?: (WizardValidEvent) => void;
        activeStepClass?: string;
        isFieldExcluded?: (field: string, element: HTMLElement, elements: HTMLElement[]) => boolean;
        isStepSkipped?:(WizardIsStepSkipped) => boolean;
        stepClass?: string;
    }
    interface WizardStepEvent {
        step: number;
        numSteps: number;
    }
    interface WizardValidEvent {
        numSteps: number;
    }
    interface WizardIsStepSkipped {
        currentStep: number;
        numSteps: number;
        targetStep: number;
    }
    class Wizard extends core.Plugin<WizardOptions> {
        constructor(opts?: WizardOptions);
        static EXCLUDED_PLUGIN: string;
        goToStep(index: number): void;
    }
    export = Wizard;
}

// Plugins that supports popular CSS frameworks

declare namespace plugins {
    type RowSelector = (field: string, element: HTMLElement) => string;
    interface FrameworkOptions {
        defaultMessageContainer?: boolean;
        formClass: string;
        messageClass?: string;
        rowInvalidClass: string;
        // A list of CSS classes (separated by a space) that will be added to the row
        rowClasses?: string;
        rowPattern: RegExp;
        rowSelector: string | RowSelector;
        rowValidatingClass?: string;
        rowValidClass: string;
        // A CSS class added to valid element
        eleValidClass?: string;
        // A CSS class added to invalid element
        eleInvalidClass?: string;
    }
    class Framework extends core.Plugin<FrameworkOptions> {
        constructor(opts?: FrameworkOptions);
    }
}

declare module 'formvalidation/plugins/Framework' {
    export = plugins.Framework;
}

declare module 'formvalidation/plugins/Bootstrap' {
    class Bootstrap extends plugins.Framework {
        constructor(opts?: plugins.FrameworkOptions);
    }
    export = Bootstrap;
}

declare module 'formvalidation/plugins/Bootstrap3' {
    class Bootstrap3 extends plugins.Framework {
        constructor(opts?: plugins.FrameworkOptions);
    }
    export = Bootstrap3;
}

declare module 'formvalidation/plugins/Bootstrap5' {
    class Bootstrap5 extends plugins.Framework {
        constructor(opts?: plugins.FrameworkOptions);
    }
    export = Bootstrap5;
}

declare module 'formvalidation/plugins/Bulma' {
    class Bulma extends plugins.Framework {
        constructor(opts?: plugins.FrameworkOptions);
    }
    export = Bulma;
}

declare module 'formvalidation/plugins/Foundation' {
    class Foundation extends plugins.Framework {
        constructor(opts?: plugins.FrameworkOptions);
    }
    export = Foundation;
}

declare module 'formvalidation/plugins/Materialize' {
    class Materialize extends plugins.Framework {
        constructor(opts?: plugins.FrameworkOptions);
    }
    export = Materialize;
}

declare module 'formvalidation/plugins/Milligram' {
    class Milligram extends plugins.Framework {
        constructor(opts?: plugins.FrameworkOptions);
    }
    export = Milligram;
}

declare module 'formvalidation/plugins/Mini' {
    class Mini extends plugins.Framework {
        constructor(opts?: plugins.FrameworkOptions);
    }
    export = Mini;
}

declare module 'formvalidation/plugins/Mui' {
    class Mui extends plugins.Framework {
        constructor(opts?: plugins.FrameworkOptions);
    }
    export = Mui;
}

declare module 'formvalidation/plugins/Pure' {
    class Pure extends plugins.Framework {
        constructor(opts?: plugins.FrameworkOptions);
    }
    export = Pure;
}

declare module 'formvalidation/plugins/Semantic' {
    class Semantic extends plugins.Framework {
        constructor(opts?: plugins.FrameworkOptions);
    }
    export = Semantic;
}

declare module 'formvalidation/plugins/Shoelace' {
    class Shoelace extends plugins.Framework {
        constructor(opts?: plugins.FrameworkOptions);
    }
    export = Shoelace;
}

declare module 'formvalidation/plugins/Spectre' {
    class Spectre extends plugins.Framework {
        constructor(opts?: plugins.FrameworkOptions);
    }
    export = Spectre;
}

declare module 'formvalidation/plugins/Tachyons' {
    class Tachyons extends plugins.Framework {
        constructor(opts?: plugins.FrameworkOptions);
    }
    export = Tachyons;
}

declare module 'formvalidation/plugins/Turret' {
    class Turret extends plugins.Framework {
        constructor(opts?: plugins.FrameworkOptions);
    }
    export = Turret;
}

declare module 'formvalidation/plugins/Uikit' {
    class Uikit extends plugins.Framework {
        constructor(opts?: plugins.FrameworkOptions);
    }
    export = Uikit;
}

// Utils
// -----

declare module 'formvalidation/utils/call' {
    function call(functionName: ((...arg: unknown[]) => unknown) | string, args: unknown[]): unknown;
    export = call;
}

declare module 'formvalidation/utils/classSet' {
    function classSet(element: HTMLElement, classes: { [clazz: string]: boolean }): void;
    export = classSet;
}

declare module 'formvalidation/utils/closest' {
    function closest(element: HTMLElement, selector: string): HTMLElement;
    export = closest;
}

declare module 'formvalidation/utils/fetch' {
    interface FetchOptions {
        // Does it request to other domain? Default value is `false`
        crossDomain?: boolean;
        // Additional headers
        headers?: {
            [name: string]: string,
        };
        // The request method. For example, `GET` (default), `POST`
        method?: string;
        params: {
            [name: string]: unknown,
        };
    }
    function fetch(url: string, options: FetchOptions): Promise<unknown>;
    export = fetch;
}

declare module 'formvalidation/utils/format' {
    function format(message: string, parameters: string | string[]): string;
    export = format;
}

declare module 'formvalidation/utils/hasClass' {
    function hasClass(element: HTMLElement, clazz: string): boolean;
    export = hasClass;
}

declare module 'formvalidation/utils/isValidDate' {
    function isValidDate(year: number, month: number, day: number, notInFuture?: boolean): boolean;
    export = isValidDate;
}

// Validators
// ----------

declare module 'formvalidation/validators/base64' {
    function base64(): {
        validate(input: core.ValidateInput<core.ValidateOptions, core.Localization>): core.ValidateResult,
    };
    export = base64;
}

declare module 'formvalidation/validators/between' {
    interface BetweenOptions extends core.ValidateOptions {
        // Default is true
        inclusive: boolean;
        max?: number;
        min?: number;
    }
    interface BetweenLocalization extends core.Localization {
        between: {
            default: string,
            notInclusive: string,
        };
    }
    function between(): {
        validate(input: core.ValidateInput<BetweenOptions, BetweenLocalization>): core.ValidateResult,
    };
    export = between;
}

declare module 'formvalidation/validators/bic' {
    function bic(): {
        validate(input: core.ValidateInput<core.ValidateOptions, core.Localization>): core.ValidateResult,
    };
    export = bic;
}

declare module 'formvalidation/validators/blank' {
    function blank(): {
        validate(input: core.ValidateInput<core.ValidateOptions, core.Localization>): core.ValidateResult,
    };
    export = blank;
}

declare module 'formvalidation/validators/callback' {
    interface CallbackOptions extends core.ValidateOptions {
        callback: ((...arg: unknown[]) => unknown) | string;
    }
    function callback(): {
        validate(input: core.ValidateInput<CallbackOptions, core.Localization>): core.ValidateResult,
    };
    export = callback;
}

declare module 'formvalidation/validators/choice' {
    interface ChoiceOptions extends core.ValidateOptions {
        max?: number;
        min?: number;
    }
    interface ChoiceLocalization extends core.Localization {
        choice: {
            between: string,
            default: string,
            less: string,
            more: string,
        };
    }
    function choice(): {
        validate(input: core.ValidateInput<ChoiceOptions, ChoiceLocalization>): core.ValidateResult,
    };
    export = choice;
}

declare module 'formvalidation/validators/color' {
    interface ColorOptions extends core.ValidateOptions {
        // The array of valid color types
        // For example: 'hex', 'hex rgb', ['hex', 'rgb']
        type: string | string[];
    }
    function color(): {
        validate(input: core.ValidateInput<ColorOptions, core.Localization>): core.ValidateResult,
    };
    export = color;
}

declare module 'formvalidation/validators/creditCard' {
    function creditCard(): {
        validate(input: core.ValidateInput<core.ValidateOptions, core.Localization>): core.ValidateResult,
    };
    export = creditCard;
}

declare module 'formvalidation/validators/cusip' {
    function cusip(): {
        validate(input: core.ValidateInput<core.ValidateOptions, core.Localization>): core.ValidateResult,
    };
    export = cusip;
}

declare module 'formvalidation/validators/date' {
    type CompareDateCallback = () => (string | Date);
    interface DateOptions extends core.ValidateOptions {
        // The date format. Default is MM/DD/YYYY
        // The format can be:
        // - date: Consist of DD, MM, YYYY parts which are separated by the separator option
        // - date and time: The time can consist of h, m, s parts which are separated by :
        // - date, time and A (indicating AM or PM)
        format: string;
        // The maximum date
        max?: string | Date | CompareDateCallback;
        // The minimum date
        min?: string | Date | CompareDateCallback;
        // Use to separate the date, month, and year. By default, it is /
        separator?: string;
    }
    interface DateLocalization extends core.Localization {
        date: {
            default: string,
            max: string,
            min: string,
            range: string,
        };
    }
    function date(): {
        validate(input: core.ValidateInput<DateOptions, DateLocalization>): core.ValidateResult,
    };
    export = date;
}

declare module 'formvalidation/validators/different' {
    type CompareDifferentCallback = () => string;
    interface DifferentOptions extends core.ValidateOptions {
        compare: string | CompareDifferentCallback;
    }
    function different(): {
        validate(input: core.ValidateInput<DifferentOptions, core.Localization>): core.ValidateResult,
    };
    export = different;
}

declare module 'formvalidation/validators/digits' {
    function digits(): {
        validate(input: core.ValidateInput<core.ValidateOptions, core.Localization>): core.ValidateResult,
    };
    export = digits;
}

declare module 'formvalidation/validators/ean' {
    function ean(): {
        validate(input: core.ValidateInput<core.ValidateOptions, core.Localization>): core.ValidateResult,
    };
    export = ean;
}

declare module 'formvalidation/validators/ein' {
    function ein(): {
        validate(input: core.ValidateInput<core.ValidateOptions, core.Localization>): core.ValidateResult,
    };
    export = ein;
}

declare module 'formvalidation/validators/emailAddress' {
    interface EmailAddressOptions extends core.ValidateOptions {
        // Allow multiple email addresses, separated by a comma or semicolon; default is false.
        multiple?: boolean | string;
        // Regex for character or characters expected as separator between addresses
        // default is comma /[,;]/, i.e. comma or semicolon.
        separator?: string | RegExp;
    }
    function emailAddress(): {
        validate(input: core.ValidateInput<EmailAddressOptions, core.Localization>): core.ValidateResult,
    };
    export = emailAddress;
}

declare module 'formvalidation/validators/file' {
    interface FileOptions extends core.ValidateOptions {
        // The allowed extensions, separated by a comma
        extension: string;
        // The maximum number of files
        maxFiles: number;
        // The maximum size in bytes
        maxSize: number;
        // The maximum size in bytes for all files
        maxTotalSize: number;
        // The minimum number of files
        minFiles: number;
        // The minimum size in bytes
        minSize: number;
        // The minimum size in bytes for all files
        minTotalSize: number;
        // The allowed MIME type, separated by a comma
        type: string;
    }
    function file(): {
        validate(input: core.ValidateInput<FileOptions, core.Localization>): core.ValidateResult,
    };
    export = file;
}

declare module 'formvalidation/validators/greaterThan' {
    interface GreaterThanOptions extends core.ValidateOptions {
        // Default is true
        inclusive: boolean;
        message: string;
        min?: number;
    }
    interface GreaterThanLocalization extends core.Localization {
        greaterThan: {
            default: string,
            notInclusive: string,
        };
    }
    function greaterThan(): {
        validate(input: core.ValidateInput<GreaterThanOptions, GreaterThanLocalization>): core.ValidateResult,
    };
    export = greaterThan;
}

declare module 'formvalidation/validators/grid' {
    function grid(): {
        validate(input: core.ValidateInput<core.ValidateOptions, core.Localization>): core.ValidateResult,
    };
    export = grid;
}

declare module 'formvalidation/validators/hex' {
    function hex(): {
        validate(input: core.ValidateInput<core.ValidateOptions, core.Localization>): core.ValidateResult,
    };
    export = hex;
}

declare module 'formvalidation/validators/iban' {
    interface IbanOptions extends core.ValidateOptions {
        // The ISO 3166-1 country code. It can be
        // - A country code
        // - Name of field which its value defines the country code
        // - Name of callback function that returns the country code
        // - A callback function that returns the country code
        country?: string;
        // Set it to true (false) to indicate that the IBAN number must be (not be) from SEPA countries
        sepa?: boolean | string;
    }
    interface IbanLocalization extends core.Localization {
        iban: {
            countries: {
                [countryCode: string]: string,
            },
            country: string,
            default: string,
        };
    }
    function iban(): {
        validate(input: core.ValidateInput<IbanOptions, IbanLocalization>): core.ValidateResult,
    };
    export = iban;
}

declare module 'formvalidation/validators/id' {
    interface IdOptions extends core.ValidateOptions {
        // The ISO 3166-1 country code. It can be
        // - A country code
        // - A callback function that returns the country code
        country: string | (() => string);
    }
    interface IdLocalization extends core.Localization {
        id: {
            countries: {
                [countryCode: string]: string,
            },
            country: string,
            default: string,
        };
    }
    function id(): {
        validate(input: core.ValidateInput<IdOptions, IdLocalization>): core.ValidateResult,
    };
    export = id;
}

declare module 'formvalidation/validators/identical' {
    type CompareIdenticalCallback = () => string;
    interface IdenticalOptions extends core.ValidateOptions {
        compare: string | CompareIdenticalCallback;
    }
    function identical(): {
        validate(input: core.ValidateInput<IdenticalOptions, core.Localization>): core.ValidateResult,
    };
    export = identical;
}

declare module 'formvalidation/validators/imei' {
    function imei(): {
        validate(input: core.ValidateInput<core.ValidateOptions, core.Localization>): core.ValidateResult,
    };
    export = imei;
}

declare module 'formvalidation/validators/imo' {
    function imo(): {
        validate(input: core.ValidateInput<core.ValidateOptions, core.Localization>): core.ValidateResult,
    };
    export = imo;
}

declare module 'formvalidation/validators/integer' {
    interface IntegerOptions extends core.ValidateOptions {
        // The decimal separator. It's '.' by default
        decimalSeparator: string;
        // The thousands separator. It's empty by default
        thousandsSeparator: string;
    }
    function integer(): {
        validate(input: core.ValidateInput<IntegerOptions, core.Localization>): core.ValidateResult,
    };
    export = integer;
}

declare module 'formvalidation/validators/ip' {
    interface IpOptions extends core.ValidateOptions {
        // Enable IPv4 validator, default to true
        ipv4?: boolean;
        // Enable IPv6 validator, default to true
        ipv6?: boolean;
    }
    interface IpLocalization extends core.Localization {
        ip: {
            default: string,
            ipv4: string,
            ipv6: string,
        };
    }
    function ip(): {
        validate(input: core.ValidateInput<IpOptions, IpLocalization>): core.ValidateResult,
    };
    export = ip;
}

declare module 'formvalidation/validators/isbn' {
    function isbn(): {
        validate(input: core.ValidateInput<core.ValidateOptions, core.Localization>): core.ValidateResult,
    };
    export = isbn;
}

declare module 'formvalidation/validators/isin' {
    function isin(): {
        validate(input: core.ValidateInput<core.ValidateOptions, core.Localization>): core.ValidateResult,
    };
    export = isin;
}

declare module 'formvalidation/validators/ismn' {
    function ismn(): {
        validate(input: core.ValidateInput<core.ValidateOptions, core.Localization>): core.ValidateResult,
    };
    export = ismn;
}

declare module 'formvalidation/validators/issn' {
    function issn(): {
        validate(input: core.ValidateInput<core.ValidateOptions, core.Localization>): core.ValidateResult,
    };
    export = issn;
}

declare module 'formvalidation/validators/lessThan' {
    interface LessThanOptions extends core.ValidateOptions {
        // Default is true
        inclusive: boolean;
        max?: number;
    }
    interface LessThanLocalization extends core.Localization {
        lessThan: {
            default: string,
            notInclusive: string,
        };
    }
    function lessThan(): {
        validate(input: core.ValidateInput<LessThanOptions, LessThanLocalization>): core.ValidateResult,
    };
    export = lessThan;
}

declare module 'formvalidation/validators/mac' {
    function mac(): {
        validate(input: core.ValidateInput<core.ValidateOptions, core.Localization>): core.ValidateResult,
    };
    export = mac;
}

declare module 'formvalidation/validators/meid' {
    function meid(): {
        validate(input: core.ValidateInput<core.ValidateOptions, core.Localization>): core.ValidateResult,
    };
    export = meid;
}

declare module 'formvalidation/validators/notEmpty' {
    interface NotEmptyOptions extends core.ValidateOptions {
        trim?: boolean;
    }
    function notEmpty(): {
        validate(input: core.ValidateInput<NotEmptyOptions, core.Localization>): core.ValidateResult,
    };
    export = notEmpty;
}

declare module 'formvalidation/validators/numeric' {
    interface NumericOptions extends core.ValidateOptions {
        // The decimal separator. It's '.' by default
        decimalSeparator: string;
        // The thousands separator. It's empty by default
        thousandsSeparator: string;
    }
    function numeric(): {
        validate(input: core.ValidateInput<NumericOptions, core.Localization>): core.ValidateResult,
    };
    export = numeric;
}

declare module 'formvalidation/validators/phone' {
    interface PhoneOptions extends core.ValidateOptions {
        // The ISO 3166-1 country code. It can be
        // - A country code
        // - A callback function that returns the country code
        country: string | (() => string);
    }
    interface PhoneLocalization extends core.Localization {
        phone: {
            countries: {
                [countryCode: string]: string,
            },
            country: string,
            default: string,
        };
    }
    function phone(): {
        validate(input: core.ValidateInput<PhoneOptions, PhoneLocalization>): core.ValidateResult,
    };
    export = phone;
}

declare module 'formvalidation/validators/promise' {
    interface PromiseOptions extends core.ValidateOptions {
        promise: (...arg: unknown[]) => unknown | string;
    }
    function promise(): {
        validate(input: core.ValidateInput<PromiseOptions, core.Localization>): core.ValidateResult,
    };
    export = promise;
}

declare module 'formvalidation/validators/regexp' {
    interface RegexpOptions extends core.ValidateOptions {
        // If specified, flags can have any combination of JavaScript regular expression flags such as:
        // g: global match
        // i: ignore case
        // m: multiple line
        flags?: string;
        // The regular expression you need to check
        regexp: string | RegExp;
    }
    function regexp(): {
        validate(input: core.ValidateInput<RegexpOptions, core.Localization>): core.ValidateResult,
    };
    export = regexp;
}

declare module 'formvalidation/validators/remote' {
    interface RemoteOptions extends core.ValidateOptions {
        url: string;
        // Does it request to other domain? Default value is `false`
        crossDomain?: boolean;
        // By default, it will take the value `{ <fieldName>: <fieldValue> }`
        data?: Record<string, unknown> | ((...arg: unknown[]) => unknown);
        // Additional headers
        headers?: {
            [name: string]: string,
        };
        // Override the field name for the request
        name?: string;
        // Can be GET or POST (default)
        method?: string;
        // The valid key. It's `valid` by default
        // This is useful when connecting to external remote server or APIs provided by 3rd parties
        validKey?: string;
    }
    function remote(): {
        validate(input: core.ValidateInput<RemoteOptions, core.Localization>): core.ValidateResult,
    };
    export = remote;
}

declare module 'formvalidation/validators/rtn' {
    function rtn(): {
        validate(input: core.ValidateInput<core.ValidateOptions, core.Localization>): core.ValidateResult,
    };
    export = rtn;
}

declare module 'formvalidation/validators/sedol' {
    function sedol(): {
        validate(input: core.ValidateInput<core.ValidateOptions, core.Localization>): core.ValidateResult,
    };
    export = sedol;
}

declare module 'formvalidation/validators/siren' {
    function siren(): {
        validate(input: core.ValidateInput<core.ValidateOptions, core.Localization>): core.ValidateResult,
    };
    export = siren;
}

declare module 'formvalidation/validators/siret' {
    function siret(): {
        validate(input: core.ValidateInput<core.ValidateOptions, core.Localization>): core.ValidateResult,
    };
    export = siret;
}

declare module 'formvalidation/validators/step' {
    interface StepOptions extends core.ValidateOptions {
        baseValue: number;
        step: number;
    }
    interface StepLocalization extends core.Localization {
        step: {
            default: string,
        };
    }
    function step(): {
        validate(input: core.ValidateInput<StepOptions, StepLocalization>): core.ValidateResult,
    };
    export = step;
}

declare module 'formvalidation/validators/stringCase' {
    interface StringCaseOptions extends core.ValidateOptions {
        // Can be 'lower' (default) or 'upper'
        case: string;
    }
    interface StringCaseLocalization extends core.Localization {
        stringCase: {
            default: string,
            upper: string,
        };
    }
    function stringCase(): {
        validate(input: core.ValidateInput<StringCaseOptions, StringCaseLocalization>): core.ValidateResult,
    };
    export = stringCase;
}

declare module 'formvalidation/validators/stringLength' {
    interface StringLengthOptions extends core.ValidateOptions {
        // At least one of two options is required
        // The min, max keys define the number which the field value compares to. min, max can be
        // - A number
        // - Name of field which its value defines the number
        // - Name of callback function that returns the number
        // - A callback function that returns the number
        max?: number | string;
        min?: number | string;
        // Indicate the length will be calculated after trimming the value or not. It is false, by default
        trim?: boolean | string;
        // Evaluate string length in UTF-8 bytes, default to false
        utf8Bytes?: boolean | string;
    }
    interface StringLengthLocalization extends core.Localization {
        stringLength: {
            between: string,
            default: string,
            less: string,
            more: string,
        };
    }
    function stringLength(): {
        validate(input: core.ValidateInput<StringLengthOptions, StringLengthLocalization>): core.ValidateResult,
    };
    export = stringLength;
}

declare module 'formvalidation/validators/uri' {
    interface UriOptions extends core.ValidateOptions {
        // Allow the URI without protocol. Default to false
        allowEmptyProtocol?: boolean | string;
        // Allow the private and local network IP. Default to false
        allowLocal?: boolean | string;
        // The protocols, separated by a comma. Default to "http, https, ftp"
        protocol?: string;
    }
    function uri(): {
        validate(input: core.ValidateInput<UriOptions, core.Localization>): core.ValidateResult,
    };
    export = uri;
}

declare module 'formvalidation/validators/uuid' {
    interface UuidOptions extends core.ValidateOptions {
        // Can be 3, 4, 5, null
        version?: string;
    }
    interface UuidLocalization extends core.Localization {
        uuid: {
            default: string,
            version: string,
        };
    }
    function uuid(): {
        validate(input: core.ValidateInput<UuidOptions, UuidLocalization>): core.ValidateResult,
    };
    export = uuid;
}

declare module 'formvalidation/validators/vat' {
    interface VatOptions extends core.ValidateOptions {
        // The ISO 3166-1 country code. It can be
        // - A country code
        // - A callback function that returns the country code
        country: string | (() => string);
    }
    interface VatLocalization extends core.Localization {
        vat: {
            countries: {
                [countryCode: string]: string,
            },
            country: string,
            default: string,
        };
    }
    function vat(): {
        validate(input: core.ValidateInput<VatOptions, VatLocalization>): core.ValidateResult,
    };
    export = vat;
}

declare module 'formvalidation/validators/vin' {
    function vin(): {
        validate(input: core.ValidateInput<core.ValidateOptions, core.Localization>): core.ValidateResult,
    };
    export = vin;
}

declare module 'formvalidation/validators/zipCode' {
    interface ZipCodeOptions extends core.ValidateOptions {
        // The ISO 3166-1 country code. It can be
        // - A country code
        // - A callback function that returns the country code
        country: string | (() => string);
    }
    interface ZipCodeLocalization extends core.Localization {
        zipCode: {
            countries: {
                [countryCode: string]: string,
            },
            country: string,
            default: string,
        };
    }
    function zipCode(): {
        validate(input: core.ValidateInput<ZipCodeOptions, ZipCodeLocalization>): core.ValidateResult,
    };
    export = zipCode;
}
