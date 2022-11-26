/**
 * FormValidation (https://formvalidation.io)
 * The best validation library for JavaScript
 * (c) 2013 - 2021 Nguyen Huu Phuoc <me@phuoc.ng>
 */

// This should be used with FormValidation UMD package
declare namespace FormValidation {
    // Core
    // ----

    namespace core {
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
            getPlugin(name: string): Plugin<unknown>;
            
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
            setCore(core: core.Core): Plugin<T>;
            install(): void;
            uninstall(): void;
        }
    }

    type Plugin<T> = core.Plugin<T>;

    // Algorithms
    // ----------

    namespace algorithms {
        function luhn(value: string): boolean;
        function mod11And10(value: string): boolean;
        function mod37And36(value: string, alphabet?: string): boolean;
        function verhoeff(value: number[]): boolean;
    }

    // formValidation
    // --------------

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

    // Locales
    // -------

    let locales: {};

    // Plugins
    // -------
    namespace plugins {
        interface AliasOptions {
            // Map the alias with defined validator name
            [alias: string]: string;
        }
        class Alias extends core.Plugin<AliasOptions> {
            constructor(opts?: AliasOptions);
        }

        class Aria extends core.Plugin<{}> {
            constructor();
        }

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

        class DefaultSubmit extends core.Plugin<{}> {
            constructor();
        }

        interface DependencyOptions {
            [field: string]: string;
        }
        class Dependency extends core.Plugin<DependencyOptions> {
            constructor(opts: DependencyOptions);
        }

        type ExcludedCallback = (field: string, element: HTMLElement, elements: HTMLElement[]) => boolean;
        interface ExcludedOptions {
            excluded: ExcludedCallback;
        }
        class Excluded extends core.Plugin<ExcludedOptions> {
            constructor(opts?: ExcludedOptions);
        }

        interface FieldStatusOptions {
            onStatusChanged?: (areFieldsValid: boolean) => void;
        }
        class FieldStatus extends core.Plugin<FieldStatusOptions> {
            constructor(opts?: FieldStatusOptions);
        }

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

        interface MandatoryIconOptions {
            icon: string;
        }
        class MandatoryIcon extends core.Plugin<MandatoryIconOptions> {
            constructor(opts?: MandatoryIconOptions);
        }

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

        type ContainerCallback = (field: string, element: HTMLElement) => HTMLElement;
        interface MessageOptions {
            clazz?: string;
            container?: string | ContainerCallback;
        }
        class Message extends core.Plugin<MessageOptions> {
            constructor(opts?: MessageOptions);
            static getClosestContainer(element: HTMLElement, upper: HTMLElement, pattern: RegExp): HTMLElement;
        }

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

        interface Recaptcha3TokenOptions {
            action: string;
            hiddenTokenName: string;
            language?: string;
            siteKey: string;
        }
        class Recaptcha3Token extends core.Plugin<Recaptcha3TokenOptions> {
            constructor(opts?: Recaptcha3TokenOptions);
        }

        interface SequenceOptions {
            enabled: boolean | { [field: string]: boolean };
        }
        class Sequence extends core.Plugin<SequenceOptions> {
            constructor(opts?: SequenceOptions);
        }

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

        interface SubmitButtonOptions {
            aspNetButton?: boolean;
            // Allow to query the submit button(s)
            // It's useful in case the submit button is outside of form
            buttons?: (form: HTMLFormElement) => Element[];
        }
        class SubmitButton extends core.Plugin<SubmitButtonOptions> {
            constructor(opts?: SubmitButtonOptions);
        }

        interface TooltipOptions {
            placement: string;
            trigger: string;
        }
        class Tooltip extends core.Plugin<TooltipOptions> {
            constructor(opts?: TooltipOptions);
        }

        interface TransformerOptions {
            [field: string]: {
                [validator: string]: (field: string, element: HTMLElement, validator: string) => string,
            };
        }
        class Transformer extends core.Plugin<TransformerOptions> {
            constructor(opts?: TransformerOptions);
        }

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

        // Plugins that supports popular CSS frameworks

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

        class Bootstrap extends plugins.Framework {
            constructor(opts?: plugins.FrameworkOptions);
        }
        class Bootstrap3 extends plugins.Framework {
            constructor(opts?: plugins.FrameworkOptions);
        }
        class Bootstrap5 extends plugins.Framework {
            constructor(opts?: plugins.FrameworkOptions);
        }
        class Bulma extends plugins.Framework {
            constructor(opts?: plugins.FrameworkOptions);
        }
        class Foundation extends plugins.Framework {
            constructor(opts?: plugins.FrameworkOptions);
        }
        class Materialize extends plugins.Framework {
            constructor(opts?: plugins.FrameworkOptions);
        }
        class Milligram extends plugins.Framework {
            constructor(opts?: plugins.FrameworkOptions);
        }
        class Mini extends plugins.Framework {
            constructor(opts?: plugins.FrameworkOptions);
        }
        class Mui extends plugins.Framework {
            constructor(opts?: plugins.FrameworkOptions);
        }
        class Pure extends plugins.Framework {
            constructor(opts?: plugins.FrameworkOptions);
        }
        class Semantic extends plugins.Framework {
            constructor(opts?: plugins.FrameworkOptions);
        }
        class Shoelace extends plugins.Framework {
            constructor(opts?: plugins.FrameworkOptions);
        }
        class Spectre extends plugins.Framework {
            constructor(opts?: plugins.FrameworkOptions);
        }
        class Tachyons extends plugins.Framework {
            constructor(opts?: plugins.FrameworkOptions);
        }
        class Turret extends plugins.Framework {
            constructor(opts?: plugins.FrameworkOptions);
        }
        class Uikit extends plugins.Framework {
            constructor(opts?: plugins.FrameworkOptions);
        }
    }

    // Utils
    // -----
    namespace utils {
        function call(functionName: ((...arg: unknown[]) => unknown) | string, args: unknown[]): unknown;
        function classSet(element: HTMLElement, classes: { [clazz: string]: boolean }): void;
        function closest(element: HTMLElement, selector: string): HTMLElement;

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

        function format(message: string, parameters: string | string[]): string;
        function hasClass(element: HTMLElement, clazz: string): boolean;
        function isValidDate(year: number, month: number, day: number, notInFuture?: boolean): boolean;
    }

    // Validators
    // ----------
    namespace validators {
        function base64(): {
            validate(input: core.ValidateInput<core.ValidateOptions, core.Localization>): core.ValidateResult,
        };

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

        function bic(): {
            validate(input: core.ValidateInput<core.ValidateOptions, core.Localization>): core.ValidateResult,
        };
        function blank(): {
            validate(input: core.ValidateInput<core.ValidateOptions, core.Localization>): core.ValidateResult,
        };

        interface CallbackOptions extends core.ValidateOptions {
            callback: ((...arg: unknown[]) => unknown) | string;
        }
        function callback(): {
            validate(input: core.ValidateInput<CallbackOptions, core.Localization>): core.ValidateResult,
        };

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

        interface ColorOptions extends core.ValidateOptions {
            // The array of valid color types
            // For example: 'hex', 'hex rgb', ['hex', 'rgb']
            type: string | string[];
        }
        function color(): {
            validate(input: core.ValidateInput<ColorOptions, core.Localization>): core.ValidateResult,
        };

        function creditCard(): {
            validate(input: core.ValidateInput<core.ValidateOptions, core.Localization>): core.ValidateResult,
        };
        function cusip(): {
            validate(input: core.ValidateInput<core.ValidateOptions, core.Localization>): core.ValidateResult,
        };

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

        type CompareDifferentCallback = () => string;
        interface DifferentOptions extends core.ValidateOptions {
            compare: string | CompareDifferentCallback;
        }
        function different(): {
            validate(input: core.ValidateInput<DifferentOptions, core.Localization>): core.ValidateResult,
        };

        function digits(): {
            validate(input: core.ValidateInput<core.ValidateOptions, core.Localization>): core.ValidateResult,
        };
        function ean(): {
            validate(input: core.ValidateInput<core.ValidateOptions, core.Localization>): core.ValidateResult,
        };
        function ein(): {
            validate(input: core.ValidateInput<core.ValidateOptions, core.Localization>): core.ValidateResult,
        };

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

        function grid(): {
            validate(input: core.ValidateInput<core.ValidateOptions, core.Localization>): core.ValidateResult,
        };
        function hex(): {
            validate(input: core.ValidateInput<core.ValidateOptions, core.Localization>): core.ValidateResult,
        };

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

        type CompareIdenticalCallback = () => string;
        interface IdenticalOptions extends core.ValidateOptions {
            compare: string | CompareIdenticalCallback;
        }
        function identical(): {
            validate(input: core.ValidateInput<IdenticalOptions, core.Localization>): core.ValidateResult,
        };

        function imei(): {
            validate(input: core.ValidateInput<core.ValidateOptions, core.Localization>): core.ValidateResult,
        };
        function imo(): {
            validate(input: core.ValidateInput<core.ValidateOptions, core.Localization>): core.ValidateResult,
        };

        interface IntegerOptions extends core.ValidateOptions {
            // The decimal separator. It's '.' by default
            decimalSeparator: string;
            // The thousands separator. It's empty by default
            thousandsSeparator: string;
        }
        function integer(): {
            validate(input: core.ValidateInput<IntegerOptions, core.Localization>): core.ValidateResult,
        };

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

        function isbn(): {
            validate(input: core.ValidateInput<core.ValidateOptions, core.Localization>): core.ValidateResult,
        };
        function isin(): {
            validate(input: core.ValidateInput<core.ValidateOptions, core.Localization>): core.ValidateResult,
        };
        function ismn(): {
            validate(input: core.ValidateInput<core.ValidateOptions, core.Localization>): core.ValidateResult,
        };
        function issn(): {
            validate(input: core.ValidateInput<core.ValidateOptions, core.Localization>): core.ValidateResult,
        };

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

        function mac(): {
            validate(input: core.ValidateInput<core.ValidateOptions, core.Localization>): core.ValidateResult,
        };
        function meid(): {
            validate(input: core.ValidateInput<core.ValidateOptions, core.Localization>): core.ValidateResult,
        };

        interface NotEmptyOptions extends core.ValidateOptions {
            trim?: boolean;
        }
        function notEmpty(): {
            validate(input: core.ValidateInput<NotEmptyOptions, core.Localization>): core.ValidateResult,
        };

        interface NumericOptions extends core.ValidateOptions {
            // The decimal separator. It's '.' by default
            decimalSeparator: string;
            // The thousands separator. It's empty by default
            thousandsSeparator: string;
        }
        function numeric(): {
            validate(input: core.ValidateInput<NumericOptions, core.Localization>): core.ValidateResult,
        };

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

        interface PromiseOptions extends core.ValidateOptions {
            promise: (...arg: unknown[]) => unknown | string;
        }
        function promise(): {
            validate(input: core.ValidateInput<PromiseOptions, core.Localization>): core.ValidateResult,
        };

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

        function rtn(): {
            validate(input: core.ValidateInput<core.ValidateOptions, core.Localization>): core.ValidateResult,
        };
        function sedol(): {
            validate(input: core.ValidateInput<core.ValidateOptions, core.Localization>): core.ValidateResult,
        };
        function siren(): {
            validate(input: core.ValidateInput<core.ValidateOptions, core.Localization>): core.ValidateResult,
        };
        function siret(): {
            validate(input: core.ValidateInput<core.ValidateOptions, core.Localization>): core.ValidateResult,
        };

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

        function vin(): {
            validate(input: core.ValidateInput<core.ValidateOptions, core.Localization>): core.ValidateResult,
        };

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
    }
}
